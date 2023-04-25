from typing import List
from logic.delivery.store.domain.entity.Option import Option


class Group:
    def __init__(self, _id, name, min_order_quantity, max_order_quantity, options: List[Option]):
        self._id = _id
        self.name = name
        self.min_order_quantity = min_order_quantity
        self.max_order_quantity = max_order_quantity
        self.options = options
