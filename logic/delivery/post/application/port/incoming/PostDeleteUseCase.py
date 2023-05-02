from abc import *


class PostDeleteUseCase(metaclass=ABCMeta):
    @abstractmethod
    def delete(self, post_id, handling_user_id):
        pass
