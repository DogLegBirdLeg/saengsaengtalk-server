from abc import *
from typing import List

from app.auth.Domain.Entity.User import User
from app.auth.Domain.Entity.Token import Token


class UserReader(metaclass=ABCMeta):
    @abstractmethod
    def find_user_by_id(self, user_id) -> User:
        pass

    @abstractmethod
    def find_user_by_username(self, username) -> User:
        pass

    @abstractmethod
    def is_already_exist_username(self, username) -> bool:
        pass

    @abstractmethod
    def is_already_exist_nickname(self, nickname) -> bool:
        pass


class UserWriter(metaclass=ABCMeta):
    @abstractmethod
    def save(self, user: User):
        pass

    @abstractmethod
    def update(self, user: User):
        pass


class TokenReader(metaclass=ABCMeta):
    @abstractmethod
    def find_token_by_user_id(self, user_id):
        pass

    @abstractmethod
    def find_token_by_refresh_token(self, refresh_token):
        pass


class TokenWriter(metaclass=ABCMeta):
    @abstractmethod
    def save(self, token: Token):
        pass

    @abstractmethod
    def update(self, token: Token):
        pass

    @abstractmethod
    def delete(self, user_id):
        pass
