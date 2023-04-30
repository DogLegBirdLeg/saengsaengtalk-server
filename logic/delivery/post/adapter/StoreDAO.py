from app import exceptions
from logic.delivery.post.application.IDao import IStoreDAO
from logic.delivery.post.domain.vo.store_vo import StoreVO
from bson import ObjectId


class MongoDBStoreDAO(IStoreDAO):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['delivery']

    def find_store_summary_by_id(self, store_id) -> StoreVO:
        find = {'_id': ObjectId(store_id)}
        store_json = self.db.store.find_one(find)

        if store_json is None:
            raise exceptions.NotExistResource

        return StoreVO(store_json['_id'], store_json['name'], store_json['fee'], store_json['min_order'], store_json['note'])
