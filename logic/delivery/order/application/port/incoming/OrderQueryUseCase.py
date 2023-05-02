from abc import *
from typing import List
from logic.delivery.order.domain.entity.Order import Order


class OrderQueryUseCase(metaclass=ABCMeta):
    @abstractmethod
    def get(self, post_id) -> Order:
        pass

    @abstractmethod
    def get_list(self, post_id) -> List[Order]:
        pass
