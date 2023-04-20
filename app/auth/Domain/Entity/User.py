import bcrypt

from app import exceptions


class User:
    def __init__(self, _id, name, username, pw, nickname, account_number, email):
        self._id = _id
        self.name = name
        self.username = username
        self.pw = pw
        self.pw = pw
        self.nickname = nickname
        self.account_number = account_number
        self.email = email

    def compare_pw(self, pw):
        if not bcrypt.checkpw(pw.encode('utf-8'), self.pw.encode('utf-8')):
            raise exceptions.PasswordMismatch

    @staticmethod
    def pw_hashing(pw):
        hashed_pw = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
        hashed_pw = hashed_pw.decode('utf-8')
        return hashed_pw

    @property
    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'username': self.username,
            'pw': self.pw,
            'nickname': self.nickname,
            'account_number': self.account_number,
            'email': self.email
        }