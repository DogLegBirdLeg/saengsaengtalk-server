from typing import List
from .Option import Options


class Group:
    def __init__(self, _id: str, name: str, min_order_quantity: int, max_order_quantity: int, options: Options):
        self._id = _id
        self.name = name
        self.min_order_quantity = min_order_quantity
        self.max_order_quantity = max_order_quantity
        self.options = options

    @property
    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'min_order_quantity': self.min_order_quantity,
            'max_order_quantity': self.max_order_quantity,
            'options': self.options.json
        }


class Groups:
    def __init__(self, groups: List[Group]):
        self.groups = groups

    def __getitem__(self, _id):
        for group in self.groups:
            if group._id == _id:
                return group

    @property
    def json(self):
        return [group.json for group in self.groups]
