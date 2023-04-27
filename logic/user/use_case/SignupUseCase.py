from logic.user.domain.Entity.User import User
from logic.user.domain.RepositoryInterface import UserRepository
from logic.common.email.use_case.IEmailSender import IEmailSender
from logic.common.cache.infra.CodeCache import CodeCache

from app import exceptions
from datetime import datetime

import random

LENGTH = 4
STRING_POOL = "0123456789"


class SignupEmailSendUseCase:
    def __init__(self, email_sender: IEmailSender, code_cache: CodeCache):
        self.email_sender = email_sender
        self.code_cache = code_cache

    def send_auth_email(self, email):
        auth_code = ""
        for i in range(LENGTH):
            auth_code += random.choice(STRING_POOL)
        self.email_sender.send_auth_code(email, auth_code)
        self.code_cache.save(email, auth_code)


class SignupUseCase:
    def __init__(self, user_repository: UserRepository, code_cache: CodeCache):
        self.user_repository = user_repository
        self.code_cache = code_cache

    def signup(self, auth_code, name, username, pw, nickname, account_number, email):
        cached_code = self.code_cache.get_code_by_email(email)
        if auth_code != cached_code:
            raise exceptions.NotValidAuthCode
        self.code_cache.delete(email)

        user = User(_id=int(round(datetime.today().timestamp() * 1000)),
                    name=name,
                    username=username,
                    pw=User.pw_hashing(pw),
                    nickname=nickname,
                    account_number=account_number,
                    email=email)
        try:
            self.user_repository.save(user)
        except exceptions.DuplicateKeyError:
            raise exceptions.DuplicateUser
