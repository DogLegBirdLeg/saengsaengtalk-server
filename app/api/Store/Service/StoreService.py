from typing import List

from app.api.Store.Domain.Model.Store import Store
from app.api.Store.Domain.RepositoryInterface import StoreRepository


class StoreService:
    def __init__(self, store_repository: StoreRepository):
        self.store_repository = store_repository

    def get(self, store_id: str) -> Store:
        store = self.store_repository.find_store(store_id)
        return store

    def get_list(self) -> List[Store]:
        store_list = self.store_repository.find_store_list()
        return store_list
