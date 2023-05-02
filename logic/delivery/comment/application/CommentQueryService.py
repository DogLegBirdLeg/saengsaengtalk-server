from logic.delivery.comment.application.port.incoming.CommentQueryService import CommentQueryUseCase
from logic.delivery.comment.domain.dto.CommentDto import CommentsDto, MainCommentDto
from logic.delivery.comment.application.port.outcoming.persistance.CommentRepository import CommentRepository
from typing import List


class CommentQueryService(CommentQueryUseCase):
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    def get_comments(self, post_id) -> List[MainCommentDto]:
        comments = self.comment_repository.find_all_comment_by_post_id(post_id)
        return CommentsDto.mapping(comments)
