from typing import List
from logic.delivery.store.usecase.DAOInterface import MenuDAO
from bson import ObjectId
from app import exceptions
from logic.delivery.store.domain.dto.MenuSummaryDto import MenuSummaryDto


class MongoDBMenuDAO(MenuDAO):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['delivery']

    def find_all_menu_summary_by_store_id(self, store_id) -> List[MenuSummaryDto]:
        pipe1 = {'$match': {'store_id': ObjectId(store_id)}}
        pipe2 = {
            '$lookup': {
                'from': 'option',
                'localField': 'groups',
                'foreignField': '_id',
                'as': 'groups'
            }
        }

        menus_json = list(self.db.menu.aggregate([pipe1, pipe2]))
        if menus_json is None:
            raise exceptions.NotExistMenu

        return [MenuSummaryDto.mapping(menu_json) for menu_json in menus_json]
