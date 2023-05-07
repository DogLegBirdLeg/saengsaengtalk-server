from logic.delivery.store.domain.entity.Store import Store


class StoreMapper:
    @staticmethod
    def store_mapping(store_json) -> Store:
        store = Store(str(store_json['_id']), store_json['name'], store_json['fee'], store_json['min_order'], store_json['phone_number'], store_json['logo_img_url'], store_json['note'])
        return store
