from abc import *
from logic.delivery.post.domain.entity.Post import Post


class PostUpdateDao(metaclass=ABCMeta):
    @abstractmethod
    def update_status(self, post: Post):
        pass

    @abstractmethod
    def update_content(self, post: Post):
        pass

    @abstractmethod
    def update_users(self, post: Post):
        pass
