from pymongo import MongoClient
from app import exceptions
from app.auth.Domain.RepositoryInterface import TokenWriter, TokenReader

from app.auth.util.TokenMapper import TokenMapper
from app.auth.Domain.Entity.Token import Token


class MongoDBTokenRepository(TokenReader, TokenWriter):
    def __init__(self, mongo_connection: MongoClient):
        self.db = mongo_connection['auth']

    def find_token_by_user_id(self, user_id) -> Token:
        find = {'user_id': user_id}
        token_json = self.db.token.find_one(find)

        if token_json is None:
            raise exceptions.NotExistResource

        token = TokenMapper.mapping_token(token_json)
        return token

    def find_token_by_refresh_token(self, refresh_token) -> Token:
        find = {'refresh_token': refresh_token}
        token_json = self.db.token.find_one(find)

        if token_json is None:
            raise exceptions.NotExistResource

        token = TokenMapper.mapping_token(token_json)
        return token

    def save(self, token: Token):
        self.db.token.insert_one(token.json)

    def update(self, token: Token):
        token_json = token.json
        update_data = {}
        for key in token_json.keys():
            if token_json[key] is not None:
                update_data[key] = token_json[key]

        find = {'user_id': token.user_id}

        update = {
            '$set': update_data
        }
        self.db.token.update_one(find, update)

    def delete(self, user_id):
        find = {'user_id': user_id}
        self.db.token.delete_one(find)
