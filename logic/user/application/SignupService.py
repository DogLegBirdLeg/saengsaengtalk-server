from logic.user.application.port.outgoing.CodeCacher import CodeCacher
from logic.user.application.port.incoming.SignupUseCase import SignupAuthUseCase, SignupUseCase
from logic.user.application.port.outgoing.UserRepository import UserRepository
from logic.user.domain.entity.User import User
from logic.user.util.PasswordHashing import pw_hashing
from logic.user.util.AuthCodeGenerator import generate_auth_code

from app import exceptions
from datetime import datetime, timedelta
from flask import current_app

import jwt
from blinker import signal

signup_signal = signal('signup-signal')


class SignupAuthService(SignupAuthUseCase):
    def __init__(self, code_cacher: CodeCacher):
        self.code_cacher = code_cacher

    def send_auth_email(self, email):
        auth_code = generate_auth_code()
        self.code_cacher.save(email, auth_code)
        signup_signal.send('auth_email', email=email, auth_code=auth_code)

    def validate_auth_code(self, email, auth_code):
        cached_code = self.code_cacher.get_code_by_email(email)
        if auth_code != cached_code:
            raise exceptions.NotValidAuthCode
        self.code_cacher.delete(email)

        return jwt.encode({'exp': datetime.utcnow() + timedelta(minutes=5)}, current_app.secret_key)


class SignupService(SignupUseCase):
    def __init__(self, user_repository: UserRepository, code_cacher: CodeCacher):
        self.user_repository = user_repository
        self.code_cacher = code_cacher

    def signup(self, auth_token, name, username, pw, nickname, account_number, email):
        try:
            jwt.decode(auth_token, current_app.secret_key, algorithms='HS256')
        except jwt.exceptions.DecodeError:
            raise exceptions.NotExistToken
        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.ExpiredToken

        user = User(_id=int(round(datetime.today().timestamp() * 1000)),
                    name=name,
                    username=username,
                    pw=pw_hashing(pw),
                    nickname=nickname,
                    account_number=account_number,
                    email=email)
        try:
            self.user_repository.save(user)
        except exceptions.DuplicateKeyError:
            raise exceptions.DuplicateUser
