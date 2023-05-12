from abc import *
from typing import List
from logic.delivery.post.dto.persistance import Post


class PostQueryUseCase(metaclass=ABCMeta):
    @abstractmethod
    def get_list(self, option, user_id) -> List[Post]:
        pass

    @abstractmethod
    def get(self, post_id) -> Post:
        pass

    @abstractmethod
    def get_owner_user_account_number(self, post_id, handling_user_id):
        pass
