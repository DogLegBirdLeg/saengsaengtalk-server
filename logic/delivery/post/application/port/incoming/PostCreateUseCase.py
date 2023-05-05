from abc import *
from logic.delivery.post.dto.presentation import PostWriteModel


class PostCreateUseCase(metaclass=ABCMeta):
    @abstractmethod
    def create(self, user_id, nickname, post_write_model: PostWriteModel) -> str:
        pass
