import pymongo.errors
from pymongo import MongoClient
from app import exceptions
from logic.user.domain.RepositoryInterface import UserRepository

from logic.user.util.Mapper import UserMapper
from logic.user.domain.Entity.User import User


class MongoDBUserRepository(UserRepository):
    def __init__(self, mongodb_connection: MongoClient):
        self.db = mongodb_connection['auth']

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

    def find_user_by_email(self, email) -> User:
        find = {'email': email}
        user_json = self.db.user.find_one(find)

        if user_json is None:
            raise exceptions.NotExistUser

        user = UserMapper.mapping_user(user_json)
        return user

    def save(self, user: User):
        try:
            self.db.user.insert_one(user.json)
        except pymongo.errors.DuplicateKeyError:
            raise exceptions.DuplicateUser

    def delete(self, user_id):
        find = {'_id': user_id}
        self.db.user.delete_one(find)
