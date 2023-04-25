from pymongo import MongoClient
from bson import ObjectId
from app import exceptions
from typing import List

from logic.delivery.store.domain.entity.Menu import Menu
from logic.delivery.store.util.MenuMapper import MenuMapper
from logic.delivery.store.domain.RepositoryInterface import MenuRepository


class MongoDBMenuRepository(MenuRepository):
    def __init__(self, mongo_connection: MongoClient):
        self.db = mongo_connection['delivery']

    def find_menu_by_id(self, _id) -> Menu:
        pipe1 = {'$match': {'_id': ObjectId(_id)}}
        pipe2 = {
            '$lookup': {
                'from': 'option',
                'localField': 'groups',
                'foreignField': '_id',
                'as': 'groups'
            }
        }

        menu_json = list(self.db.menu.aggregate([pipe1, pipe2]))
        if menu_json is None:
            raise exceptions.NotExistMenu

        return MenuMapper.menu_mapping(menu_json[0])

    def find_all_menu_by_store_id(self, store_id: str) -> List[Menu]:
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
        if len(menus_json) == 0:
            raise exceptions.NotExistStore

        return [MenuMapper.menu_mapping(menu_json) for menu_json in menus_json]