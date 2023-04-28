from flask import request
from dependency_injector.wiring import inject, Provide
from src.post_container import PostContainer
from flask_restx import Namespace, Resource, fields
from datetime import datetime

from logic.delivery.post.usecase.PostUseCase \
    import PostQueryUseCase, PostCreateUseCase, PostDeleteUseCase, PostUpdateUseCase

post_ns = Namespace('post', description='게시글')

from app.api.store import store_model
post_model = post_ns.model('게시글', {
    '_id': fields.String(description='게시글 ID', example='63da17abcc800e43227d91e4'),
    'title': fields.String(decscription='게시글 제목', example='[15:30] 네네치킨'),
    'user_id': fields.Integer(description='작성자 ID', example='1674995732373'),
    'nickname': fields.String(description='작성자 닉네임', example='개발이'),
    'place': fields.String(description='주문 장소', example='기숙사'),
    'min_member': fields.Integer(description='최소 주문 인원', example=3),
    'max_member': fields.Integer(description='최대 주문 인원', example=6),
    'order_time': fields.DateTime(description='주문 시간', example='2023-02-22T08:56:57'),
    'store': fields.Nested(store_model),
    'status': fields.String(description='현재 게시글 상태', example='recruiting'),
    'users': fields.List(fields.Integer(description='유저 ID', example=1674995732373))
})
from app.api.order import order_model
post_format_model = post_ns.model('게시글 포멧', {
    'store_id': fields.String(description='가게 ID', example='644bb4cc735de5ca8a93c365'),
    'place': fields.String(description='수령 장소', example='기숙사'),
    'order_time': fields.DateTime(description='주문 시간', example=datetime.today().strftime("%Y-%m-%dT%H:%M:%S")),
    'min_member': fields.Integer(description='최소 주문 인원', example=3),
    'max_member': fields.Integer(description='최대 주문 인원', example=6),
    'order': fields.Nested(model=order_model)
})
post_update_format_model = post_ns.model('게시글 수정 포멧', {
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

option = post_ns.parser()
option.add_argument('option', type=str, help='필터링 옵션', choices=('all', 'joinable', 'joined'))


@post_ns.route('')
class Post(Resource):
    @post_ns.doc(security='jwt', parser=option, description="현재 작성된 게시글 목록을 반환합니다")
    @post_ns.marshal_list_with(code=200, description='조회 결과', fields=post_model, mask=None)
    @inject
    def get(self, post_use_case: PostQueryUseCase = Provide[PostContainer.post_query_use_case]):
        """게시글 목록 조회"""
        option = request.args['option']

        posts = post_use_case.get_list(option)
        return [post.json for post in posts]

    @post_ns.doc(security='jwt', body=post_format_model, description="게시글을 작성합니다")
    @post_ns.marshal_with(code=201, description='등록 성공', fields=post_register_model, mask=None)
    @inject
    def post(self, post_use_case: PostCreateUseCase = Provide[PostContainer.post_create_use_case]):
        """게시글 작성"""
        data = request.get_json()
        store_id = data['store_id']
        place = data['place']
        order_time = data['order_time']
        min_member = int(data['min_member'])
        max_member = int(data['max_member'])
        order = data['order']

        post_id = post_use_case.create(store_id, place, order_time, min_member, max_member, order)
        return {'post_id': post_id}, 201


@post_ns.route('/<string:post_id>')
class PostDetail(Resource):
    @post_ns.doc(security='jwt', description="게시글 상세 정보를 반환합니다")
    @post_ns.marshal_with(code=200, description='조회 결과', fields=post_model, mask=None)
    @inject
    def get(self, post_id, post_use_case: PostQueryUseCase = Provide[PostContainer.post_query_use_case]):
        """게시글 상세 조회"""
        post = post_use_case.get(post_id)

        post_json = post.json

        return post_json

    @post_ns.doc(security='jwt', body=post_update_format_model, description="게시글을 수정합니다")
    @post_ns.response(code=204, description='수정 성공')
    @inject
    def patch(self, post_id, post_use_case: PostUpdateUseCase = Provide[PostContainer.post_update_use_case]):
        """게시글 수정"""
        data = request.get_json()
        post_use_case.modify(post_id, data['order_time'], data['place'], int(data['min_member']), int(data['max_member']))
        return '', 204

    @post_ns.doc(security='jwt', description="게시글을 삭제합니다")
    @post_ns.response(code=204, description='삭제 성공')
    @inject
    def delete(self, post_id, post_use_case: PostDeleteUseCase = Provide[PostContainer.post_delete_use_case]):
        """게시글 삭제"""
        post_use_case.delete(post_id)
        return '', 204


@post_ns.route('/<string:post_id>/status')
class PostStatus(Resource):
    @post_ns.doc(security='jwt', body=post_status_model, description="상태를 변경합니다, recruiting/closed/ordered/delivered 중 하나 입력")
    @post_ns.response(code=204, description='변경 성공')
    @inject
    def patch(self, post_id, post_use_case: PostUpdateUseCase = Provide[PostContainer.post_update_use_case]):
        """게시글 상태 변경"""
        data = request.get_json()
        post_use_case.change_status(post_id, data['status'])
        return '', 204
