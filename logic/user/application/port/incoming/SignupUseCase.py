from abc import *


class SignupAuthUseCase(metaclass=ABCMeta):
    @abstractmethod
    def send_auth_email(self, email):
        pass

    @abstractmethod
    def validate_auth_code(self, email, auth_code):
        pass


class SignupUseCase(metaclass=ABCMeta):
    @abstractmethod
    def signup(self, auth_token, name, username, pw, nickname, account_number, email):
        pass
