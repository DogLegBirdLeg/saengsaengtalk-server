import jwt
from datetime import datetime, timedelta
from app import exceptions


class Token:
    def __init__(self, user_id, access_token, refresh_token, registration_token):
        self.user_id = user_id
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.registration_token = registration_token

    @staticmethod
    def decode_token(token, secret_key):
        try:
            payload = jwt.decode(token, secret_key, algorithms='HS256')
        except jwt.exceptions.DecodeError:
            raise exceptions.TokenDecodeFail

        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.ExpiredToken

        return payload

    @staticmethod
    def create_access_token(user_id, nickname, secret_key):
        payload = {
            'user_id': user_id,
            'nickname': nickname,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }

        return jwt.encode(payload, secret_key)

    @staticmethod
    def create_refresh_token(user_id, nickname, secret_key):
        payload = {
            'user_id': user_id,
            'nickname': nickname,
        }

        return jwt.encode(payload, secret_key)

    @property
    def json(self):
        return {
            'user_id': self.user_id,
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'registration_token': self.registration_token
        }
