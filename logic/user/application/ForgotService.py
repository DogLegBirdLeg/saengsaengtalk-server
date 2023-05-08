from app import exceptions
import jwt
from datetime import datetime, timedelta
from flask import current_app

from logic.user.application.port.outgoing.CodeCacher import CodeCacher
from logic.user.application.port.outgoing.UserRepository import UserRepository
from logic.user.application.port.incoming.ForgotUseCase import ForgotUsernameUseCase, ForgotPasswordUseCase
from logic.user.util.AuthCodeGenerator import generate_auth_code

from blinker import signal

forgot_signal = signal('forgot-signal')


class ForgotUsernameService(ForgotUsernameUseCase):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def send_username_email(self, email):
        try:
            user = self.user_repository.find_user_by_email(email)
        except exceptions.NotExistResource:
            raise exceptions.NotExistUser

        forgot_signal.send('username', email=email, username=user.username)


class ForgotPasswordService(ForgotPasswordUseCase):
    def __init__(self, code_cacher: CodeCacher, user_repository: UserRepository):
        self.code_cacher = code_cacher
        self.user_repository = user_repository

    def send_auth_email(self, email):
        auth_code = generate_auth_code()
        self.code_cacher.save(email, auth_code)
        forgot_signal.send('auth_email', email=email, auth_code=auth_code)

    def publish_temp_access_token(self, auth_code, email):
        cached_code = self.code_cacher.get_code_by_email(email)
        if auth_code != cached_code:
            raise exceptions.NotValidAuthCode
        self.code_cacher.delete(email)

        try:
            user = self.user_repository.find_user_by_email(email)
        except exceptions.NotExistResource:
            raise exceptions.NotExistUser

        payload = {
            'user_id': user._id,
            'nickname': user.nickname,
            'exp': datetime.utcnow() + timedelta(minutes=10)
        }

        return jwt.encode(payload, current_app.secret_key)
