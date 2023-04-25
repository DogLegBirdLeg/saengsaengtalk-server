from logic.delivery.order.domain.entity.OrderOption import OrderOption
from typing import List


class OrderGroup:
    def __init__(self, _id, name, min_order_quantity, max_order_quantity, order_options: List[OrderOption]):
        self._id = _id
        self.name = name
        self.min_order_quantity = min_order_quantity
        self.max_order_quantity = max_order_quantity
        self.order_options = order_options
