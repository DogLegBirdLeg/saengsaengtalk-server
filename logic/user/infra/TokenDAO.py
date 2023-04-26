from abc import *
from app import exceptions


class TokenDAO(metaclass=ABCMeta):
    @abstractmethod
    def find_token_by_user_id(self, user_id):
        pass

    @abstractmethod
    def find_token_by_refresh_token(self, refresh_token):
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

    @abstractmethod
    def delete(self, user_id):
        pass


class MongoDBTokenDAO(TokenDAO):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['auth']

    def find_token_by_user_id(self, user_id):
        find = {'user._id': user_id}
        token = self.db.token.find_one(find)
        if token is None:
            raise exceptions.NotExistResource
        return token

    def find_token_by_refresh_token(self, refresh_token):
        find = {'refresh_token': refresh_token}
        token = self.db.token.find_one(find)
        if token is None:
            raise exceptions.NotExistResource
        return token

    def save(self, user_id, access_token, refresh_token, registration_token):
        find = {'_id': user_id}
        user = self.db.user.find_one(find)

        data = {
            'user': user,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'registration_token': registration_token,
        }

        self.db.token.insert_one(data)

    def update_access_token(self, user_id, access_token):
        find = {'user._id': user_id}
        update = {
            '$set': {'access_token': access_token}
        }

        self.db.token.update_one(find, update)

    def update_registration_token(self, user_id, registration_token):
        find = {'user._id': user_id}
        update = {
            '$set': {'registration_token': registration_token}
        }

        self.db.token.update_one(find, update)

    def delete(self, user_id):
        find = {'user._id': user_id}
        self.db.token.delete_one(find)
