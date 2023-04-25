from abc import *
from typing import List
from logic.delivery.store.domain.entity.Menu import Menu
from logic.delivery.store.domain.entity.Store import Store


class StoreRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_store_by_id(self, store_id) -> Store:
        pass

    @abstractmethod
    def find_all_store(self) -> List[Store]:
        pass


class MenuRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_menu_by_id(self, menu_id) -> Menu:
        pass

    @abstractmethod
    def find_all_menu_by_store_id(self, store_id) -> List[Menu]:
        pass
