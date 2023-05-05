from abc import *


class CommentCreateUseCase(metaclass=ABCMeta):
    @abstractmethod
    def create_comment(self, user_id, nickname, post_id, content):
        pass

    @abstractmethod
    def create_reply(self, user_id, nickname, post_id, parent_id, content):
        pass
