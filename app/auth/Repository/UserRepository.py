import pymongo.errors
from pymongo import MongoClient
from app import exceptions
from app.auth.Domain.RepositoryInterface import UserReader, UserWriter

from app.auth.util.Mapper import UserMapper
from app.auth.Domain.Entity.User import User


class MongoDBUserRepository(UserReader, UserWriter):
    def __init__(self, mongo_connection: MongoClient):
        self.db = mongo_connection['auth']

    def find_user_by_id(self, user_id) -> User:
        find = {'_id': user_id}
        user_json = self.db.user.find_one(find)

        if user_json is None:
            raise exceptions.NotExistUser

        user = UserMapper.mapping_user(user_json)
        return user

    def find_user_by_username(self, username) -> User:
        find = {'username': username}
        user_json = self.db.user.find_one(find)

        if user_json is None:
            raise exceptions.NotExistUser

        user = UserMapper.mapping_user(user_json)
        return user

    def is_already_exist_username(self, username) -> bool:
        find = {'username': username}
        user_json = self.db.user.find_one(find)
        return user_json is not None

    def is_already_exist_nickname(self, nickname) -> bool:
        find = {'nickname': nickname}
        user_json = self.db.user.find_one(find)
        return user_json is not None

    def save(self, user: User):
        try:
            self.db.user.insert_one(user.json)
        except pymongo.errors.DuplicateKeyError:
            raise exceptions.DuplicateUser

    def update(self, user: User):
        user_json = user.json
        for key, value in user_json.popitem():
            if value is None:
                del user_json[key]

        find = {'_id': user._id}

        update = {
            '$set': user_json
        }
        self.db.user.update_one(find, update)
