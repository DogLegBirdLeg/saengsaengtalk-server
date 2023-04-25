from logic.delivery.store.domain.entity.Menu import Menu
from logic.delivery.store.domain.entity.Group import Group
from logic.delivery.store.domain.entity.Option import Option
from typing import List


class OptionDto:
    def __init__(self, _id, name, price):
        self._id = _id
        self.name = name
        self.price = price

    @property
    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'price': self.price
        }

    @staticmethod
    def mapping(option: Option):
        return OptionDto(_id=option._id,
                         name=option.name,
                         price=option.price)


class GroupDto:
    def __init__(self, _id, name, min_order_quantity, max_order_quantity, options: List[OptionDto]):
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
            'options': [option.json for option in self.options]
        }

    @staticmethod
    def mapping(group: Group):
        return GroupDto(_id=group._id,
                        name=group.name,
                        min_order_quantity=group.min_order_quantity,
                        max_order_quantity=group.max_order_quantity,
                        options=[OptionDto.mapping(option) for option in group.options])


class MenuDto:
    def __init__(self, _id, section, name, price, groups: List[GroupDto]):
        self._id = _id
        self.section = section
        self.name = name
        self.price = price
        self.groups = groups

    @property
    def json(self):
        return {
            '_id': self._id,
            'section': self.section,
            'name': self.name,
            'price': self.price,
            'groups': [group.json for group in self.groups]
        }

    @staticmethod
    def mapping(menu: Menu):
        return MenuDto(_id=menu._id,
                       section=menu.section,
                       name=menu.name,
                       price=menu.price,
                       groups=[GroupDto.mapping(group) for group in menu.groups])