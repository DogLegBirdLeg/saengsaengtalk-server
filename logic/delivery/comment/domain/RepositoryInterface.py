from abc import *
from typing import List
from logic.delivery.comment.domain.entity.Comment import Comment


class CommentRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_comment_by_id(self, _id) -> Comment:
        pass

    @abstractmethod
    def find_all_comment_by_post_id(self, post_id) -> List[Comment]:
        pass

    @abstractmethod
    def save(self, comment: Comment):
        pass

    @abstractmethod
    def delete(self, _id):
        pass
