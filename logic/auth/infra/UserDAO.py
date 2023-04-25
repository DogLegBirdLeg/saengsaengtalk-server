from abc import *


class UserDAO(metaclass=ABCMeta):
    @abstractmethod
    def is_already_exist_username(self, username) -> bool:
        pass

    @abstractmethod
    def is_already_exist_nickname(self, nickname) -> bool:
        pass


class MongoDBUserDAO(UserDAO):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['auth']

    def is_already_exist_username(self, username) -> bool:
        find = {'username': username}
        user_json = self.db.user.find_one(find)
        return user_json is not None

    def is_already_exist_nickname(self, nickname) -> bool:
        find = {'nickname': nickname}
        user_json = self.db.user.find_one(find)
        return user_json is not None
