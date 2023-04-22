from abc import *
from typing import List
from app.api.Store.Domain.Model.Store import Store
from app.api.Store.Domain.Model.MenuSummary import MenuSummary
from app.api.Store.Domain.Model.Menu import Menu, Menus


class StoreRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_store_list(self) -> List[Store]:
        pass

    @abstractmethod
    def find_store(self, store_id) -> Store:
        pass


class MenuRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_menu_list(self, store_id) -> Menus:
        pass

    @abstractmethod
    def find_menu_summary_list(self, store_id) -> List[MenuSummary]:
        pass

    @abstractmethod
    def find_menu(self, _id) -> Menu:
        pass
