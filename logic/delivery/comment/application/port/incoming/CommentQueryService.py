from abc import *
from typing import List
from logic.delivery.comment.domain.entity.Comment import Comment


class CommentQueryUseCase(metaclass=ABCMeta):
    @abstractmethod
    def get_comments(self, post_id) -> List[Comment]:
        pass
