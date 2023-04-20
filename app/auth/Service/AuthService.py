from app.auth.Domain.Entity.User import User
from app.auth.Domain.Entity.Token import Token
from app.auth.Domain.RepositoryInterface import UserReader, UserWriter, TokenReader, TokenWriter
from flask import current_app
from app import exceptions
from datetime import datetime


class AuthService:
    def __init__(self, user_reader: UserReader, user_writer: UserWriter, token_reader: TokenReader, token_writer: TokenWriter):
        self.user_reader = user_reader
        self.user_writer = user_writer
        self.token_reader = token_reader
        self.token_writer = token_writer

    def signup(self, auth_code, name, username, pw, nickname, account_number, email):
        if current_app.config['AUTH_CODE'] != auth_code:
            raise exceptions.NotValidAuthCode
        user = User(_id=int(round(datetime.today().timestamp() * 1000)),
                    name=name,
                    username=username,
                    pw=User.pw_hashing(pw),
                    nickname=nickname,
                    account_number=account_number,
                    email=email)

        self.user_writer.save(user)

    def check_field(self, field, value) -> bool:
        if field == 'username':
            return self.user_reader.is_already_exist_username(value)

        elif field == 'nickname':
            return self.user_reader.is_already_exist_nickname(value)

    def signin(self, username, pw, registration_token) -> (Token, User):
        try:
            user = self.user_reader.find_user_by_username(username)
        except exceptions.NotExistResource:
            raise exceptions.NotExistUser

        user.compare_pw(pw)

        try:
            token = self.token_reader.find_token_by_user_id(user._id)
        except exceptions.NotExistResource:
            access_token = Token.create_access_token(user._id, user.nickname, current_app.secret_key)
            refresh_token = Token.create_refresh_token(user._id, user.nickname, current_app.secret_key)
            token = Token(user._id, access_token, refresh_token, registration_token)

            self.token_writer.save(token)
            return token, user

        token.registration_token = registration_token
        self.token_writer.update(token)
        return token, user

    def refresh(self, refresh_token):
        try:
            token = self.token_reader.find_token_by_refresh_token(refresh_token)
        except exceptions.NotExistResource:
            raise exceptions.NotExistToken

        payload = Token.decode_token(refresh_token, current_app.secret_key)

        access_token = Token.create_access_token(payload['user_id'], payload['nickname'], current_app.secret_key)
        token = Token(payload['user_id'], access_token, refresh_token, None)
        self.token_writer.update(token)

        return access_token

    def logout(self, access_token):
        payload = Token.decode_token(access_token, current_app.secret_key)
        self.token_writer.delete(payload['user_id'])
