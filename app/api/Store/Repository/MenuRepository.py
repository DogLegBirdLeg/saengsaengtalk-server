from pymongo import MongoClient
from bson import ObjectId
from app import exceptions
from typing import List

from app.api.Store.Domain.RepositoryInterface import MenuRepository
from app.api.Store.Domain.Model.Menu import Menu, Menus
from app.api.Store.Domain.Model.MenuSummary import MenuSummary
from app.api.Store.util.MenuMapper import MenuMapper, MenuSummaryMapper


class MongoDBMenuRepository(MenuRepository):
    def __init__(self, mongo_connection: MongoClient):
        self.db = mongo_connection['delivery']

    def find_menu_list(self, store_id: str) -> Menus:
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

        return MenuMapper.menus_mapping(menus_json)

    def find_menu_summary_list(self, store_id) -> List[MenuSummary]:
        find = {'store_id': ObjectId(store_id)}
        projection = {'groups': False}

        menus_json = list(self.db.menu.find(find, projection))
        if len(menus_json) == 0:
            raise exceptions.NotExistStore

        return [MenuSummaryMapper.menu_mapping(menu_json) for menu_json in menus_json]

    def find_menu(self, _id) -> Menu:
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
