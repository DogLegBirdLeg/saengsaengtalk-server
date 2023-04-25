from logic.auth.domain.Entity.User import User
from logic.auth.domain.RepositoryInterface import UserRepository
from logic.auth.use_case.EmailSenderInterface import EmailSenderInterface
from logic.auth.infra.UserDAO import UserDAO
from logic.auth.infra.CodeCache import CodeCache

from app import exceptions
from datetime import datetime


class SignupUseCase:
    def __init__(self, user_repository: UserRepository, user_dao: UserDAO, email_sender: EmailSenderInterface, code_cache: CodeCache):
        self.user_repository = user_repository
        self.user_dao = user_dao
        self.email_sender = email_sender
        self.code_cache = code_cache

    def send_auth_email(self, email):
        auth_code = self.email_sender.send_auth_email(email)
        self.code_cache.save(auth_code, email)

    def signup(self, auth_code, name, username, pw, nickname, account_number, email):
        cached_email = self.code_cache.get_email_by_code(auth_code)
        if email != cached_email:
            raise exceptions.NotValidAuthCode
        self.code_cache.delete(auth_code)

        user = User(_id=int(round(datetime.today().timestamp() * 1000)),
                    name=name,
                    username=username,
                    pw=User.pw_hashing(pw),
                    nickname=nickname,
                    account_number=account_number,
                    email=email)

        self.user_repository.save(user)

    def check_field(self, field, value) -> bool:
        if field == 'username':
            return self.user_dao.is_already_exist_username(value)

        elif field == 'nickname':
            return self.user_dao.is_already_exist_nickname(value)
