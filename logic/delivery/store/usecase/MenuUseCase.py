from logic.delivery.store.domain.dto.SectionDto import Sections
from logic.delivery.store.domain.dto.MenuDto import MenuDto
from logic.delivery.store.domain.RepositoryInterface import MenuRepository
from logic.delivery.store.usecase.DAOInterface import MenuDAO


class MenuUseCase:
    def __init__(self, menu_repository: MenuRepository, menu_dao: MenuDAO):
        self.menu_repository = menu_repository
        self.menu_dao = menu_dao

    def get(self, menu_id: str) -> MenuDto:
        menu = self.menu_repository.find_menu_by_id(menu_id)
        return MenuDto.mapping(menu)

    def get_summary_list(self, store_id) -> Sections:
        menus = self.menu_dao.find_all_menu_summary_by_store_id(store_id)
        sections = Sections(menus)

        return sections
