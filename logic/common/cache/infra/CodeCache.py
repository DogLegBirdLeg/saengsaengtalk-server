from logic.common.cache.use_case.ICodeCache import CodeCache
from redis import StrictRedis


class RedisCodeCache(CodeCache):
    def __init__(self, redis_connection: StrictRedis):
        self.db = redis_connection

    def get_code_by_email(self, email) -> str:
        return self.db.get(email)

    def save(self, email, code):
        self.db.set(email, code)

    def delete(self, email):
        self.db.delete(email)
