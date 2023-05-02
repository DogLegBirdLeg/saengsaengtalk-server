from app import exceptions
from flask import current_app
import jwt
from datetime import datetime, timedelta

from logic.user.application.port.incoming.AuthUseCase import AuthUseCase
from logic.user.application.port.outgoing.UserRepository import UserRepository
from logic.user.application.port.outgoing.TokenDao import TokenDao


class JwtAuthService(AuthUseCase):
    def __init__(self, user_repository: UserRepository, token_dao: TokenDao):
        self.user_repository = user_repository
        self.token_dao = token_dao

    def login(self, username, pw, registration_token):
        try:
            user = self.user_repository.find_user_by_username(username)
        except exceptions.NotExistResource:
            raise exceptions.SigninFail

        if user.compare_pw(pw) is False:
            raise exceptions.SigninFail

        try:
            token = self.token_dao.find_token_by_user_id(user._id)
        except exceptions.NotExistResource:
            access_token = self._create_token(user._id, user.nickname, current_app.secret_key, True)
            refresh_token = self._create_token(user._id, user.nickname, current_app.secret_key)
            self.token_dao.save(user._id, access_token, refresh_token, registration_token)
            return access_token, refresh_token

        self.token_dao.update_registration_token(user._id, registration_token)
        return token['access_token'], token['refresh_token']

    def logout(self, user_id):
        self.token_dao.delete(user_id)

    def refresh(self, refresh_token) -> str:
        try:
            token = self.token_dao.find_token_by_refresh_token(refresh_token)
        except exceptions.NotExistResource:
            raise exceptions.NotExistToken

        user = token['user']
        access_token = self._create_token(user['_id'], user['nickname'], current_app.secret_key, True)
        self.token_dao.update_access_token(user['_id'], access_token)
        return access_token

    @staticmethod
    def _create_token(user_id, nickname, secret_key, expire_time: bool = False):
        if expire_time is True:
            payload = {
                'user_id': user_id,
                'nickname': nickname,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }
            return jwt.encode(payload, secret_key)

        payload = {
            'user_id': user_id,
            'nickname': nickname,
        }
        return jwt.encode(payload, secret_key)
