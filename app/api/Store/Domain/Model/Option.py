from typing import List


class Option:
    def __init__(self, _id: str, name: str, price: int):
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


class Options:
    def __init__(self, options: List[Option]):
        self.options = options

    def __getitem__(self, _id):
        for option in self.options:
            if option._id == _id:
                return option

    @property
    def json(self):
        return [option.json for option in self.options]
