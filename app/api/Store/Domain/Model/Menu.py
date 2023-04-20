from typing import List
from .Group import Groups


class Menu:
    def __init__(self, _id: str, section: str, name: str, price: int, groups: Groups):
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
            'groups': self.groups.json
        }


class Menus:
    def __init__(self, menus: List[Menu]):
        self.menus = menus

    def __getitem__(self, _id):
        for menu in self.menus:
            if menu._id == _id:
                return menu

    @property
    def json(self):
        return [menu.json for menu in self.menus]
