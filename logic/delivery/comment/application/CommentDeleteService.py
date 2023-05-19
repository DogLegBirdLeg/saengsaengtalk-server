from logic.delivery.comment.application.port.outcoming.persistance.CommentRepository import CommentRepository
from logic.delivery.comment.application.port.incoming.CommentDeleteUseCase import CommentDeleteUseCase
import exceptions


class CommentDeleteService(CommentDeleteUseCase):
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    def delete(self, user_id, comment_id):
        try:
            comment = self.comment_repository.find_comment_by_id(comment_id)
        except exceptions.NotExistResource:
            raise exceptions.NotExistComment

        comment.delete(user_id)
        self.comment_repository.delete(comment_id)
