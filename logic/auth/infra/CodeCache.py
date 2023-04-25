from abc import *
from redis import StrictRedis


class CodeCache(metaclass=ABCMeta):
    @abstractmethod
    def get_email_by_code(self, code) -> str:
        pass

    @abstractmethod
    def save(self, code, email):
        pass

    @abstractmethod
    def delete(self, code):
        pass


class RedisCodeCache(CodeCache):
    def __init__(self, redis_connection: StrictRedis):
        self.db = redis_connection

    def get_email_by_code(self, code) -> str:
        return self.db.get(code)

    def save(self, code, email):
        self.db.set(code, email)

    def delete(self, code):
        self.db.delete(code)
