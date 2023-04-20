from app.api.Order.Domain.Entity.OrderOption import OrderOption
from typing import List


class OrderGroup:
    def __init__(self, _id, name, min_order_quantity, max_order_quantity, order_options: List[OrderOption]):
        self._id = _id
        self.name = name
        self.min_order_quantity = min_order_quantity
        self.max_order_quantity = max_order_quantity
        self.order_options = order_options

    @property
    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'min_order_quantity': self.min_order_quantity,
            'max_order_quantity': self.max_order_quantity,
            'options': [order_option.json for order_option in self.order_options]
        }