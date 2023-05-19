from pymongo import MongoClient
from bson import ObjectId
import exceptions
from typing import List

from logic.delivery.store.domain.entity.Menu import Menu
from logic.delivery.store.util.MenuMapper import MenuMapper
from logic.delivery.store.domain.RepositoryInterface import MenuRepository


class MongoDBMenuRepository(MenuRepository):
    def __init__(self, mongo_connection: MongoClient):
        self.db = mongo_connection['delivery']

    def find_menu_by_id(self, _id) -> Menu:
        find = {'_id': ObjectId(_id)}

        menu_json = self.db.menu.find_one(find)

        if menu_json is None:
            raise exceptions.NotExistMenu

        return MenuMapper.menu_mapping(menu_json)

    def find_all_menu_by_store_id(self, store_id: str) -> List[Menu]:
        find = {'store_id': ObjectId(store_id)}
        menus_json = list(self.db.menu.find(find))

        if len(menus_json) == 0:
            raise exceptions.NotExistStore

        return [MenuMapper.menu_mapping(menu_json) for menu_json in menus_json]
