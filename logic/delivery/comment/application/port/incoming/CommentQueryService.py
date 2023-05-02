from abc import *
from typing import List
from logic.delivery.comment.domain.dto.CommentDto import MainCommentDto


class CommentQueryUseCase(metaclass=ABCMeta):
    @abstractmethod
    def get_comments(self, post_id) -> List[MainCommentDto]:
        pass
