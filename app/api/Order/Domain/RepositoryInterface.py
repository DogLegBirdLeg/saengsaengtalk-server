from abc import *
from typing import List

from app.api.Order.Domain.Entity.Order import Order


class OrderRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_order_by_user_id(self, post_id, user_id) -> Order:
        pass

    @abstractmethod
    def find_order_list_by_post_id(self, post_id) -> List[Order]:
        pass

    @abstractmethod
    def find_post_join_user(self):
        pass

    @abstractmethod
    def save(self, post_id, order: Order):
        pass

    @abstractmethod
    def delete(self, post_id, user_id):
        pass

    @abstractmethod
    def delete_post(self, post_id):
        pass
