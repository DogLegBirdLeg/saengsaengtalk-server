from abc import *
from redis import StrictRedis


class CodeCache(metaclass=ABCMeta):
    @abstractmethod
    def get_code_by_email(self, email) -> str:
        pass

    @abstractmethod
    def save(self, email, code):
        pass

    @abstractmethod
    def delete(self, email):
        pass


class RedisCodeCache(CodeCache):
    def __init__(self, redis_connection: StrictRedis):
        self.db = redis_connection

    def get_code_by_email(self, email) -> str:
        return self.db.get(email)

    def save(self, email, code):
        self.db.set(email, code)

    def delete(self, email):
        self.db.delete(email)
