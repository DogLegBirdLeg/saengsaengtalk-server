from abc import *


class CommentDeleteUseCase(metaclass=ABCMeta):
    @abstractmethod
    def delete(self, user_id, comment_id):
        pass
