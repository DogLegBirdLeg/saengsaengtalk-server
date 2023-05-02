from flask import request
from flask_restx import Namespace, Resource, fields
from flask import g
from dependency_injector.wiring import inject, Provide
from src.comment_container import CommentContainer
from logic.delivery.comment.application.port.incoming.CommentQueryService import CommentQueryUseCase
from logic.delivery.comment.application.port.incoming.CommentCreateUseCase import CommentCreateUseCase
from logic.delivery.comment.application.port.incoming.CommentDeleteUseCase import CommentDeleteUseCase

comment_ns = Namespace('comment', description='댓글')

sub_comment_model = comment_ns.model('대댓글', {
    '_id': fields.String(description='댓글 ID', example='6447d6884c5c7f0de2717ec4'),
    'post_id': fields.String(description='게시글 ID', example='6447d6884c5c7f0de2717ec3'),
    'create_at': fields.String(description='시간', example='2023-04-30T19:10:50'),
    'user_id': fields.Integer(description='유저 ID', example=1674995732373),
    'nickname': fields.String(description='닉네임', example='개발이여친'),
    'status': fields.String(description='상태', example='created'),
    'content': fields.String(description='내용', example='이건 대댓글임')
})

main_comment_model = comment_ns.model('댓글', {
    '_id': fields.String(description='댓글 ID', example='6447d6884c5c7f0de2717ec1'),
    'post_id': fields.String(description='게시글 ID', example='6447d6884c5c7f0de2717ec2'),
    'create_at': fields.String(description='시간', example='2023-04-30T19:10:50'),
    'user_id': fields.Integer(description='유저 ID', example=1674995732373),
    'nickname': fields.String(description='닉네임', example='개발이'),
    'status': fields.String(description='상태', example='created'),
    'content': fields.String(description='내용', example='이건 댓글임'),
    'sub_comments': fields.List(fields.Nested(model=sub_comment_model))
})

content_model = comment_ns.model('댓글 작성', {
    'content': fields.String(descripton='내용', example='댓글 쓸거임')
})


@comment_ns.route('/<string:post_id>/comments')
class Comment(Resource):
    @comment_ns.doc(security='jwt', description="게시글의 모든 댓글을 반환합니다")
    @comment_ns.marshal_with(code=200, fields=comment_ns.model('댓글 조회 응답', {
        'comments': fields.List(fields.Nested(model=main_comment_model))
    }), mask=None)
    @inject
    def get(self, post_id, comment_use_case: CommentQueryUseCase = Provide[CommentContainer.comment_query_service]):
        """댓글 조회"""
        comments = comment_use_case.get_comments(post_id)

        return {'comments': [comment.json for comment in comments]}

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
