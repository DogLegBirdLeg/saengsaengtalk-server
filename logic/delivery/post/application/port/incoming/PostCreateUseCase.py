from abc import *


class PostCreateUseCase(metaclass=ABCMeta):
    @abstractmethod
    def create(self, user_id, nickname, store_id, place, order_time, min_member, max_member, order_json) -> str:
        pass
