from logic.delivery.store.domain.entity.Store import Store


class StoreDto:
    def __init__(self, _id: str, name: str, fee: int, min_order: int):
        self._id = _id
        self.name = name
        self.fee = fee
        self.min_order = min_order

    @property
    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'fee': self.fee,
            'min_order': self.min_order
        }

    @staticmethod
    def mapping(store: Store):
        return StoreDto(_id=store._id,
                        name=store.name,
                        fee=store.fee,
                        min_order=store.min_order)
