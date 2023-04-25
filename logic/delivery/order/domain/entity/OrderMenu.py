from typing import List
from logic.delivery.order.domain.entity.OrderGroup import OrderGroup


class OrderMenu:
    def __init__(self, _id, name, price, order_groups: List[OrderGroup]):
        self._id = _id
        self.name = name
        self.price = price
        self.order_groups = order_groups
