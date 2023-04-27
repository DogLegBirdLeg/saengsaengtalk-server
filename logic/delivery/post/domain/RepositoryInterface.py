from abc import *

from logic.delivery.post.domain.entity.Post import Post


class IPostRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_post_by_id(self, post_id) -> Post:
        pass

    @abstractmethod
    def save(self, post: Post):
        pass

    @abstractmethod
    def delete(self, post_id):
        pass
