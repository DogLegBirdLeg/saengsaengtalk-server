from abc import *
from logic.delivery.post.dto.presentation import PostUpdateModel


class PostUpdateUseCase(metaclass=ABCMeta):
    @abstractmethod
    def modify(self, user_id, post_id, post_update_model: PostUpdateModel):
        pass

    @abstractmethod
    def change_status(self, user_id, post_id, status):
        pass

    @abstractmethod
    def update_fee(self, user_id, post_id, fee):
        pass
