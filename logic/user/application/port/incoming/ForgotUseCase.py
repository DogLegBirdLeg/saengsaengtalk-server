from abc import *


class ForgotUsernameUseCase(metaclass=ABCMeta):
    @abstractmethod
    def send_username_email(self, email):
        pass


class ForgotPasswordUseCase(metaclass=ABCMeta):
    @abstractmethod
    def send_auth_email(self, email):
        pass

    @abstractmethod
    def publish_temp_access_token(self, auth_code, email):
        pass
    