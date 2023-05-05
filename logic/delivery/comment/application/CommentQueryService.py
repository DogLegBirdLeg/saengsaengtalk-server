from logic.delivery.comment.application.port.incoming.CommentQueryService import CommentQueryUseCase
from logic.delivery.comment.domain.entity.Comment import Comment
from logic.delivery.comment.application.port.outcoming.persistance.CommentRepository import CommentRepository
from typing import List


class CommentQueryService(CommentQueryUseCase):
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    def get_comments(self, post_id) -> List[Comment]:
        comments = self.comment_repository.find_all_comment_by_post_id(post_id)

        def find_super_comment(comments: List[Comment]):
            for comment in comments:
                if comment.supper_comment_id is None:
                    comments.remove(comment)
                    return comment

        def find_sub_comment(comments: List[Comment], comment_id):
            for comment in comments:
                if comment.supper_comment_id == comment_id:
                    comments.remove(comment)
                    return comment

        temp_comments = []
        while len(comments) > 0:
            super_comment = find_super_comment(comments)
            print(super_comment)
            temp_comments.append(super_comment)

            sub_comment = find_sub_comment(comments, super_comment._id)
            while sub_comment is not None:
                temp_comments.append(sub_comment)
                sub_comment = find_sub_comment(comments, super_comment._id)

        return temp_comments
