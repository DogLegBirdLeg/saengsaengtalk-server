from logic.delivery.comment.application.port.incoming.CommentCreateUseCase import CommentCreateUseCase
from logic.delivery.comment.domain.entity.Comment import Comment
from logic.delivery.comment.application.port.outcoming.persistance.CommentRepository import CommentRepository
from bson import ObjectId


class CommentCreateService(CommentCreateUseCase):
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    def create_comment(self, user_id, nickname, post_id, content):
        comment = Comment(_id=str(ObjectId()),
                          post_id=post_id,
                          user_id=user_id,
                          nickname=nickname,
                          status='created',
                          content=content)

        self.comment_repository.save(comment)

    def create_reply(self, user_id, nickname, post_id, super_comment_id, content):
        comment = Comment(_id=str(ObjectId()),
                          post_id=post_id,
                          user_id=user_id,
                          nickname=nickname,
                          status='created',
                          content=content,
                          super_comment_id=super_comment_id)
        self.comment_repository.save(comment)
