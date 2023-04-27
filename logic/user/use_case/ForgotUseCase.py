from logic.common.cache.infra.CodeCache import CodeCache
from logic.common.email.use_case.IEmailSender import IEmailSender
from logic.user.domain.RepositoryInterface import UserRepository
from app import exceptions
import jwt
from datetime import datetime, timedelta
from flask import current_app

import random

LENGTH = 4
STRING_POOL = "0123456789"


class ForgotEmailSendUseCase:
    def __init__(self, code_cache: CodeCache, email_sender: IEmailSender, user_repository: UserRepository):
        self.code_cache = code_cache
        self.email_sender = email_sender
        self.user_repository = user_repository

    def send_username_email(self, email):
        user = self.user_repository.find_user_by_email(email)
        self.email_sender.send_username(user.email, user.username)

    def send_auth_email(self, email):
        auth_code = ""
        for i in range(LENGTH):
            auth_code += random.choice(STRING_POOL)
        self.email_sender.send_auth_code(email, auth_code)
        self.code_cache.save(email, auth_code)


class ForgotTempTokenPublishUseCase:
    def __init__(self, code_cache: CodeCache, user_repository: UserRepository):
        self.code_cache = code_cache
        self.user_repository = user_repository

    def publish_temp_access_token(self, auth_code, email):
        cached_code = self.code_cache.get_code_by_email(email)
        if auth_code != cached_code:
            raise exceptions.NotValidAuthCode
        self.code_cache.delete(email)

        user = self.user_repository.find_user_by_email(email)
        payload = {
            'user_id': user._id,
            'nickname': user.nickname,
            'exp': datetime.utcnow() + timedelta(minutes=10)
        }

        return jwt.encode(payload, current_app.secret_key)
