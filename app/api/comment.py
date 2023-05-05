from flask import request
from flask_restx import Namespace, Resource, fields
from flask import g
from dependency_injector.wiring import inject, Provide
from src.comment_container import CommentContainer
from logic.delivery.comment.application.port.incoming.CommentQueryService import CommentQueryUseCase
from logic.delivery.comment.application.port.incoming.CommentCreateUseCase import CommentCreateUseCase
from logic.delivery.comment.application.port.incoming.CommentDeleteUseCase import CommentDeleteUseCase
from logic.delivery.comment.util.JsonConverter import comment_to_json
from datetime import datetime
comment_ns = Namespace('comment', description='댓글')


class NullableString(fields.String):
    __schema_type__ = ['string', 'null']
    __schema_example__ = 'nullable string'


comment_model = comment_ns.model('댓글', {
    '_id': fields.String(description='댓글 ID', example='6447d6884c5c7f0de2717ec1'),
    'post_id': fields.String(description='게시글 ID', example='6447d6884c5c7f0de2717ec2'),
    'create_at': fields.DateTime(description='시간', example=datetime.today().strftime("%Y-%m-%dT%H:%M:%S")),
    'user_id': fields.Integer(description='유저 ID', example=1674995732373),
    'nickname': fields.String(description='닉네임', example='개발이'),
    'status': fields.String(description='상태', example='created'),
    'content': fields.String(description='내용', example='이건 댓글임'),
    'super_comment_id': NullableString(description='부모 댓글 ID', example='6447d6884c5c7f0de2717ec0')
})

content_model = comment_ns.model('댓글 작성', {
    'content': fields.String(descripton='내용', example='댓글 쓸거임')
})


@comment_ns.route('/<string:post_id>/comments')
class Comment(Resource):
    @comment_ns.doc(security='jwt', description="게시글의 모든 댓글을 반환합니다")
    @comment_ns.response(code=200, fields=comment_ns.model('댓글 조회 응답', {
        'comments': fields.List(fields.Nested(model=comment_model))
    }), description="조회 성공")
    @inject
    def get(self, post_id, comment_use_case: CommentQueryUseCase = Provide[CommentContainer.comment_query_service]):
        """댓글 조회"""
        comments = comment_use_case.get_comments(post_id)
        temp = []
        for comment in comments:
            comment_json = comment_to_json(comment)
            comment_json['create_at'] = comment.create_at.strftime('%Y-%m-%dT%H:%M:%S')
            temp.append(comment_json)

        return {'comments': temp}

    @comment_ns.doc(security='jwt', body=content_model, description="댓글을 작성합니다")
    @comment_ns.response(code=204, description='작성 성공')
    @inject
    def post(self, post_id, comment_use_case: CommentCreateUseCase = Provide[CommentContainer.comment_create_service]):
        """댓글 작성"""
        data = request.get_json()

        comment_use_case.create_comment(g.id, g.nickname, post_id, data['content'])
        return '', 204


@comment_ns.route('/<string:post_id>/comments/<string:comment_id>')
class CommentDetail(Resource):
    @comment_ns.doc(security='jwt', body=content_model, description="대댓글을 작성합니다")
    @comment_ns.response(code=204, description='작성 성공')
    @inject
    def post(self, post_id, comment_id, comment_use_case: CommentCreateUseCase = Provide[CommentContainer.comment_create_service]):
        """대댓글 작성"""
        data = request.get_json()

        comment_use_case.create_reply(g.id, g.nickname, post_id, comment_id, data['content'])
        return '', 204

    @comment_ns.doc(security='jwt', description="댓글을 삭제합니다")
    @comment_ns.response(code=204, description='삭제 성공')
    @inject
    def delete(self, post_id, comment_id, comment_use_case: CommentDeleteUseCase = Provide[CommentContainer.comment_delete_service]):
        """댓글 삭제"""
        comment_use_case.delete(g.id, comment_id)
        return '', 204
