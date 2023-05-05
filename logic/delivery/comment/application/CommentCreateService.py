from logic.delivery.comment.application.port.incoming.CommentCreateUseCase import CommentCreateUseCase
from logic.delivery.comment.domain.entity.Comment import Comment
from logic.delivery.comment.application.port.outcoming.persistance.CommentRepository import CommentRepository
from bson import ObjectId
from datetime import datetime


class CommentCreateService(CommentCreateUseCase):
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    def create_comment(self, user_id, nickname, post_id, content):
        current = datetime.now()
        create_at = datetime(year=current.year, month=current.month, day=current.day, hour=current.hour, minute=current.minute, second=current.second)
        comment = Comment(_id=str(ObjectId()),
                          post_id=post_id,
                          create_at=create_at,
                          user_id=user_id,
                          nickname=nickname,
                          status='created',
                          content=content)

        self.comment_repository.save(comment)

    def create_reply(self, user_id, nickname, post_id, super_comment_id, content):
        current = datetime.now()
        create_at = datetime(year=current.year, month=current.month, day=current.day, hour=current.hour, minute=current.minute, second=current.second)
        comment = Comment(_id=str(ObjectId()),
                          post_id=post_id,
                          create_at=create_at,
                          user_id=user_id,
                          nickname=nickname,
                          status='created',
                          content=content,
                          super_comment_id=super_comment_id)
        self.comment_repository.save(comment)
