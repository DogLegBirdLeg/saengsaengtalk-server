from typing import List

from logic.delivery.store.domain.dto.StoreDto import StoreDto
from logic.delivery.store.domain.RepositoryInterface import StoreRepository


class StoreUseCase:
    def __init__(self, store_repository: StoreRepository):
        self.store_repository = store_repository

    def get(self, store_id: str) -> StoreDto:
        store = self.store_repository.find_store_by_id(store_id)
        return StoreDto.mapping(store)

    def get_list(self) -> List[StoreDto]:
        stores = self.store_repository.find_all_store()
        return [StoreDto.mapping(store) for store in stores]
