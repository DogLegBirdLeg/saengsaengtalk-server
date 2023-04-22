from pymongo import MongoClient
from bson import ObjectId
from app import exceptions
from typing import List

from app.api.Store.Domain.Model.Store import Store
from app.api.Store.Domain.RepositoryInterface import StoreRepository
from app.api.Store.util.StoreMapper import StoreMapper


class MongoDBStoreRepository(StoreRepository):
    def __init__(self, mongo_connection: MongoClient):
        self.db = mongo_connection['delivery']

    def find_store_list(self) -> List[Store]:
        stores_json = list(self.db.store.find())

        store_list = [StoreMapper.store_mapping(store_json) for store_json in stores_json]

        return store_list

    def find_store(self, store_id: str) -> Store:
        find = {'_id': ObjectId(store_id)}
        store_json = self.db.store.find_one(find)

        if store_json is None:
            raise exceptions.NotExistStore

        store = StoreMapper.store_mapping(store_json)

        return store
