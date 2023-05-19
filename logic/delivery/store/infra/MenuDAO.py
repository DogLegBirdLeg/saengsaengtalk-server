from typing import List
from logic.delivery.store.usecase.DAOInterface import MenuDAO
from bson import ObjectId
import exceptions
from logic.delivery.store.domain.dto.MenuSummaryDto import MenuSummaryDto


class MongoDBMenuDAO(MenuDAO):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['delivery']

    def find_all_menu_summary_by_store_id(self, store_id) -> List[MenuSummaryDto]:
        find = {'store_id': ObjectId(store_id)}
        projection = {'groups': False}

        menus_json = list(self.db.menu.find(find, projection))
        if menus_json is None:
            raise exceptions.NotExistMenu

        return [MenuSummaryDto.mapping(menu_json) for menu_json in menus_json]
