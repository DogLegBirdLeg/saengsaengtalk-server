from logic.user.infra.CodeCache import CodeCache
from logic.user.infra.EmailSender import EmailSenderInterface
from logic.user.domain.RepositoryInterface import UserRepository
from app import exceptions
import jwt
from datetime import datetime, timedelta
from flask import current_app


class ForgotUseCase:
    def __init__(self, code_cache: CodeCache, email_sender: EmailSenderInterface, user_repository: UserRepository):
        self.code_cache = code_cache
        self.email_sender = email_sender
        self.user_repository = user_repository

    def send_username_email(self, email):
        user = self.user_repository.find_user_by_email(email)
        self.email_sender.send_username_email(user.email, user.username)

    def send_auth_email(self, email):
        auth_code = self.email_sender.send_auth_email(email)
        self.code_cache.save(email, auth_code)

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
