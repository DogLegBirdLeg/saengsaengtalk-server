from abc import *


class AuthUseCase(metaclass=ABCMeta):
    @abstractmethod
    def login(self, username, pw, registration_token):
        pass

    @abstractmethod
    def logout(self, user_id, access_token):
        pass
