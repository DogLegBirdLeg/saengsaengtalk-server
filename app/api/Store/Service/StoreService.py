from typing import List

from app.api.Store.Domain.Model.Store import Store
from app.api.Store.Domain.RepositoryInterface import StoreReader


class StoreService:
    def __init__(self, store_reader: StoreReader):
        self.store_reader = store_reader

    def get(self, store_id: str) -> Store:
        store = self.store_reader.find_store(store_id)
        return store

    def get_list(self) -> List[Store]:
        store_list = self.store_reader.find_store_list()
        return store_list
