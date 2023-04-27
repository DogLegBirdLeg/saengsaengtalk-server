from abc import *


class IEmailSender(metaclass=ABCMeta):
    @abstractmethod
    def send_auth_code(self, email, auth_code) -> str:
        pass

    @abstractmethod
    def send_username(self, email, username):
        pass
