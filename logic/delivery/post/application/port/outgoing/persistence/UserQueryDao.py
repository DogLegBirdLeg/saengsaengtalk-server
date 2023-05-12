from abc import *


class UserQueryDao(metaclass=ABCMeta):
    @abstractmethod
    def find_user_account_number(self, user_id):
        pass
