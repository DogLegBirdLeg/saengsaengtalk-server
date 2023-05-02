from abc import *


class PostUserPoolUseCase:
    @abstractmethod
    def join(self, post_id, user_id, nickname, order_json):
        pass

    @abstractmethod
    def quit(self, post_id, user_id):
        pass
