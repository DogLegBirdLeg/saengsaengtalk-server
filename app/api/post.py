from flask import request, g
from dependency_injector.wiring import inject, Provide
from src.post_container import PostContainer
from flask_restx import Namespace, Resource, fields
from datetime import datetime

from logic.delivery.post.application.port.incoming.PostCreateUseCase import PostCreateUseCase
from logic.delivery.post.application.port.incoming.PostQueryUseCase import PostQueryUseCase
from logic.delivery.post.application.port.incoming.PostDeleteUseCase import PostDeleteUseCase
from logic.delivery.post.application.port.incoming.PostUpdateUseCase import PostUpdateUseCase

from logic.delivery.post.dto.presentation import PostWriteModel, PostUpdateModel

post_ns = Namespace('post', description='게시글')

from app.api.store import store_model
post_model = post_ns.model('게시글', {
    '_id': fields.String(description='게시글 ID', example='63da17abcc800e43227d91e4'),
    'user_id': fields.Integer(description='작성자 ID', example='1674995732373'),
    'nickname': fields.String(description='작성자 닉네임', example='개발이'),
    'place': fields.String(description='주문 장소', example='기숙사'),
    'min_member': fields.Integer(description='최소 주문 인원', example=3),
    'max_member': fields.Integer(description='최대 주문 인원', example=6),
    'order_time': fields.DateTime(description='주문 시간', example='2023-02-22T08:56:57'),
    'fee': fields.Integer(description='배달비', example=3000),
    'store': fields.Nested(store_model),
    'status': fields.String(description='현재 게시글 상태', example='recruiting'),
    'users': fields.List(fields.Integer(description='유저 ID', example=1674995732373))
})
from app.api.order import order_model
post_format_model = post_ns.model('게시글 작성', {
    'store_id': fields.String(description='가게 ID', example='644bb4cc735de5ca8a93c365'),
    'place': fields.String(description='수령 장소', example='기숙사'),
    'order_time': fields.DateTime(description='주문 시간', example=datetime.today().strftime("%Y-%m-%dT%H:%M:%S")),
    'min_member': fields.Integer(description='최소 주문 인원', example=3),
    'max_member': fields.Integer(description='최대 주문 인원', example=6),
    'order': fields.Nested(model=order_model)
})
post_update_format_model = post_ns.model('게시글 수정', {
     'order_time': fields.DateTime(description='주문 시간', example='2023-02-04T02:07:10'),
     'place': fields.String(description='수령 장소', example='생자대 앞'),
     'min_member': fields.Integer(description='최소 주문 인원', example=2),
     'max_member': fields.Integer(description='최대 주문 인원', example=5)
})
post_register_model = post_ns.model('게시글 등록 응답', {
    'post_id': fields.String(description='등록된 포스트의 ID', example='63da17abcc800e43227d91e4')
})
post_status_model = post_ns.model('상태 파라미터', {
    'status': fields.String(description='상태 변경, recruiting/closed/ordered/delivered', example='closed'),
})
post_fee_model = post_ns.model('배달비 수정', {
    'fee': fields.Integer(description='배달비', example=5000),
})

option = post_ns.parser()
option.add_argument('option', type=str, help='필터링 옵션', choices=('all', 'joinable', 'joined'))


@post_ns.route('')
class Post(Resource):
    @post_ns.doc(security='jwt', parser=option, description="현재 작성된 게시글 목록을 반환합니다")
    @post_ns.marshal_list_with(code=200, description='조회 결과', fields=post_model, mask=None)
    @inject
    def get(self, post_use_case: PostQueryUseCase = Provide[PostContainer.post_query_service]):
        """게시글 목록 조회"""
        option = request.args['option']

        posts = post_use_case.get_list(option, g.id)
        return [post.json for post in posts]

    @post_ns.doc(security='jwt', body=post_format_model, description="게시글을 작성합니다")
    @post_ns.marshal_with(code=201, description='등록 성공', fields=post_register_model, mask=None)
    @inject
    def post(self, post_use_case: PostCreateUseCase = Provide[PostContainer.post_create_service]):
        """게시글 작성"""
        data = request.get_json()
        post_write_model = PostWriteModel(**data)
        post_id = post_use_case.create(g.id, g.nickname, post_write_model)
        return {'post_id': post_id}, 201


@post_ns.route('/<string:post_id>')
class PostDetail(Resource):
    @post_ns.doc(security='jwt', description="게시글 상세 정보를 반환합니다")
    @post_ns.marshal_with(code=200, description='조회 결과', fields=post_model, mask=None)
    @inject
    def get(self, post_id, post_use_case: PostQueryUseCase = Provide[PostContainer.post_query_service]):
        """게시글 상세 조회"""
        post = post_use_case.get(post_id)
        return post.json

    @post_ns.doc(security='jwt', body=post_update_format_model, description="게시글을 수정합니다")
    @post_ns.response(code=204, description='수정 성공')
    @inject
    def patch(self, post_id, post_use_case: PostUpdateUseCase = Provide[PostContainer.post_update_service]):
        """게시글 수정"""
        data = request.get_json()
        post_update_model = PostUpdateModel(**data)
        post_use_case.modify(g.id, post_id, post_update_model)
        return '', 204

    @post_ns.doc(security='jwt', description="게시글을 삭제합니다")
    @post_ns.response(code=204, description='삭제 성공')
    @inject
    def delete(self, post_id, post_use_case: PostDeleteUseCase = Provide[PostContainer.post_delete_service]):
        """게시글 삭제"""
        post_use_case.delete(post_id, g.id)
        return '', 204


@post_ns.route('/<string:post_id>/status')
class PostStatus(Resource):
    @post_ns.doc(security='jwt', body=post_status_model, description="상태를 변경합니다, recruiting/closed/ordered/delivered 중 하나 입력")
    @post_ns.response(code=204, description='변경 성공')
    @inject
    def patch(self, post_id, post_use_case: PostUpdateUseCase = Provide[PostContainer.post_update_service]):
        """게시글 상태 변경"""
        data = request.get_json()
        post_use_case.change_status(g.id, post_id, data['status'])
        return '', 204


@post_ns.route('/<string:post_id>/fee')
class PostFee(Resource):
    @post_ns.doc(security='jwt', body=post_fee_model, description="해당 게시글의 주문에서 발생한 배달비를 수정합니다")
    @post_ns.response(code=204, description='변경 성공')
    @inject
    def patch(self, post_id, post_use_case: PostUpdateUseCase = Provide[PostContainer.post_update_service]):
        """배달비 변경"""
        data = request.get_json()
        post_use_case.update_fee(g.id, post_id, data['fee'])
        return '', 204


@post_ns.route('/<string:post_id>/account-number')
class PostFee(Resource):
    @post_ns.doc(security='jwt', description="게시글 대표 유저의 계좌 정보를 확인합니다. 게시글에 참여한 유저가 배달완료 상태에서만 확인 가능합니다")
    @post_ns.response(code=200, description='조회 성공', model=post_ns.model('계좌 정보', {
        'name': fields.String(description='이름', example='김개발'),
        'account_number': fields.String(description='계좌번호', example='123-1234-1234-12 농협')
    }))
    @inject
    def get(self, post_id, post_use_case: PostQueryUseCase = Provide[PostContainer.post_query_service]):
        """대표 유저 계좌 정보 확인"""
        name, account_number = post_use_case.get_owner_user_account_number(post_id, g.id)
        return {'account_number': account_number}
