from abc import *
from typing import List

from app.api.Post.Domain.Entity.Post import Post
from app.api.Order.Domain.Entity.Order import Order


class HistoryRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_post_history_list(self, user_id) -> List[Post]:
        pass

    @abstractmethod
    def find_order_history_list(self, post_id) -> List[Order]:
        pass
