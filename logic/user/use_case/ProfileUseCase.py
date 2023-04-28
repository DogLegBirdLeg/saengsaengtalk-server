from logic.user.domain.RepositoryInterface import UserRepository
from logic.user.infra.UserDAO import UserDAO
from logic.user.domain.Entity.User import User
from flask import g
from app import exceptions


class ProfileQueryUseCase:
    def __init__(self, user_repository: UserRepository, user_dao: UserDAO):
        self.user_repository = user_repository
        self.user_dao = user_dao

    def get(self):
        return self.user_repository.find_user_by_id(g.id)


class ProfileDeleteUseCase:
    def __init__(self, user_repository: UserRepository, user_dao: UserDAO):
        self.user_repository = user_repository
        self.user_dao = user_dao

    def delete(self):
        self.user_repository.delete(g.id)


class ProfileUpdateUseCase:
    def __init__(self, user_repository: UserRepository, user_dao: UserDAO):
        self.user_repository = user_repository
        self.user_dao = user_dao

    def update_password(self, new_password):
        hashed_pw = User.pw_hashing(new_password)
        self.user_dao.update_pw(g.id, hashed_pw)

    def update_nickname(self, nickname):
        self.user_dao.update_nickname(g.id, nickname)

    def update_account_number(self, account_number):
        self.user_dao.update_account_number(g.id, account_number)
