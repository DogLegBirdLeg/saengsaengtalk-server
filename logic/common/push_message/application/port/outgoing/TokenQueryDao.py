from abc import *
from typing import List


class TokenQueryDao(metaclass=ABCMeta):
    @abstractmethod
    def find_all_registration_token_user_id(self, users: List[int]):
        pass

    @abstractmethod
    def find_registration_token_by_user_id(self, user_id):
        pass
