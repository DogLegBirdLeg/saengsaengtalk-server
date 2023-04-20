from typing import List


class MenuSummary:
    def __init__(self, _id: str, section: str, name: str, price: int):
        self._id = _id
        self.section = section
        self.name = name
        self.price = price

    @property
    def json(self):
        return {
            '_id': self._id,
            'section': self.section,
            'name': self.name,
            'price': self.price,
        }


class MenusSummary:
    def __init__(self, menus: List[MenuSummary]):
        self.menus = menus

    @property
    def json(self):
        return [menu.json for menu in self.menus]
