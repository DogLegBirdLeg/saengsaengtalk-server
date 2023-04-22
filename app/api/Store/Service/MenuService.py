from app.api.Store.Domain.Model.Section import Sections
from app.api.Store.Domain.Model.Menu import Menu, Menus
from app.api.Store.Domain.RepositoryInterface import MenuRepository


class MenuService:
    def __init__(self, menu_repository: MenuRepository):
        self.menu_repository = menu_repository

    def get(self, menu_id: str) -> Menu:
        menu = self.menu_repository.find_menu(menu_id)
        return menu

    def get_list(self, store_id) -> Menus:
        menu_list = self.menu_repository.find_menu_list(store_id)
        return menu_list

    def get_summary_list(self, store_id) -> Sections:
        menu_summary_list = self.menu_repository.find_menu_summary_list(store_id)
        sections = Sections(menu_summary_list)

        return sections
