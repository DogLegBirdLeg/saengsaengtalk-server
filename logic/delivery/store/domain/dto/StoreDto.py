from logic.delivery.store.domain.entity.Store import Store


class StoreDto:
    def __init__(self, _id: str, name: str, fee: int, min_order: int, phone_number , logo_img_url, note: str):
        self._id = _id
        self.name = name
        self.fee = fee
        self.min_order = min_order
        self.phone_number = phone_number
        self.logo_img_url = logo_img_url
        self.note = note

    @property
    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'fee': self.fee,
            'min_order': self.min_order,
            'phone_number': self.phone_number,
            'logo_img_url': self.logo_img_url,
            'note': self.note
        }

    @staticmethod
    def mapping(store: Store):
        return StoreDto(_id=store._id,
                        name=store.name,
                        fee=store.fee,
                        min_order=store.min_order,
                        phone_number=store.phone_number,
                        logo_img_url=store.logo_img_url,
                        note=store.note)
