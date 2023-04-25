from typing import List
from logic.delivery.store.domain.entity.Group import Group


class Menu:
    def __init__(self, _id, section, name, price, groups: List[Group]):
        self._id = _id
        self.section = section
        self.name = name
        self.price = price
        self.groups = groups
