class Store:
    def __init__(self, _id: str, name: str, fee: int, min_order: int, phone_number, note: str):
        self._id = _id
        self.name = name
        self.fee = fee
        self.min_order = min_order
        self.phone_number = phone_number
        self.note = note
