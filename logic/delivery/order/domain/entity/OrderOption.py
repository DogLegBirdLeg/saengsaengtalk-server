class OrderOption:
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