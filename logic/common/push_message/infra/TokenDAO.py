from abc import *


class ITokenDAO(metaclass=ABCMeta):
    @abstractmethod
    def find_all_registration_token_user_id(self, users):
        pass


class MongoDBTokenDAO(ITokenDAO):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['auth']

    def find_all_registration_token_user_id(self, users):
        find = {
            'user._id': {'$in': users}
        }
        projection = {'_id': False, 'registration_token': True}

        tokens = [token['registration_token'] for token in self.db.token.find(find, projection)]
        return tokens
