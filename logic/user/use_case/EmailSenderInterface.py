from abc import *


class EmailSenderInterface(metaclass=ABCMeta):
    @abstractmethod
    def send_auth_email(self, email) -> str:
        pass

    @abstractmethod
    def send_username_email(self, email, username):
        pass
