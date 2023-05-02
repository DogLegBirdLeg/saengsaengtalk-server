from abc import *
from typing import List


class TokenQueryDao(metaclass=ABCMeta):
    @abstractmethod
    def find_all_registration_token_user_id(self, users: List[int]):
        pass
