from app import exceptions
from logic.delivery.post.usecase.DAOInterface import StoreDAO
from logic.delivery.post.domain.vo.store_vo import StoreVO
from bson import ObjectId


class MongoDBStoreDAO(StoreDAO):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['delivery']

    def find_store_summary_by_id(self, store_id) -> StoreVO:
        find = {'_id': ObjectId(store_id)}
        store_json = self.db.store.find_one(find)
        print(find)
        if store_json is None:
            raise exceptions.NotExistStore

        return StoreVO(store_json['_id'], store_json['name'], store_json['fee'], store_json['min_order'])
