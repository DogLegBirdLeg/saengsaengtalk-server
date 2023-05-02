from abc import *


class PostUpdateUseCase(metaclass=ABCMeta):
    @abstractmethod
    def modify(self, user_id, post_id, order_time, place, min_member, max_member):
        pass

    @abstractmethod
    def change_status(self, user_id, post_id, status):
        pass
