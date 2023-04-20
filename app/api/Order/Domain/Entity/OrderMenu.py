from typing import List
from app.api.Order.Domain.Entity.OrderGroup import OrderGroup


class OrderMenu:
    def __init__(self, _id, name, price, order_groups: List[OrderGroup]):
        self._id = _id
        self.name = name
        self.price = price
        self.order_groups = order_groups

    @property
    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'price': self.price,
            'groups': [order_group.json for order_group in self.order_groups]
        }
