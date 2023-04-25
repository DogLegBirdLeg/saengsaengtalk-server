from abc import *
from typing import Tuple


class TokenDAO(metaclass=ABCMeta):
    @abstractmethod
    def find_token_by_user_id(self, user_id) -> Tuple[str, str]:
        pass

    @abstractmethod
    def find_token_by_refresh_token(self, refresh_token) -> Tuple[str, str]:
        pass

    @abstractmethod
    def save(self, user_id, access_token, refresh_token, registration_token):
        pass

    @abstractmethod
    def update_access_token(self, user_id, access_token):
        pass

    @abstractmethod
    def update_registration_token(self, user_id, registration_token):
        pass


class MongoDBTokenDAO(TokenDAO):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['auth']

    def find_token_by_user_id(self, user_id) -> Tuple[str, str]:
        find = {'user_id': user_id}
        token = self.db.token.find_one(find)
        return token['access_token'], token['refresh_token']

    def find_token_by_refresh_token(self, refresh_token) -> Tuple[str, str]:
        find = {'refresh_token': refresh_token}
        token = self.db.token.find_one(find)
        return token['access_token'], token['refresh_token']

    def save(self, user_id, access_token, refresh_token, registration_token):
        data = {
            'user_id': user_id,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'registration_token': registration_token
        }
        self.db.token.insert_one(data)

    def update_access_token(self, user_id, access_token):
        find = {'user_id': user_id}
        update = {
            '$set': {'access_token': access_token}
        }

        self.db.token.update_one(find, update)

    def update_registration_token(self, user_id, registration_token):
        find = {'user_id': user_id}
        update = {
            '$set': {'registration_token': registration_token}
        }

        self.db.token.update_one(find, update)
