from abc import *
from typing import List

from app.api.Post.Domain.Entity.Post import Post


class PostRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_post(self, post_id) -> Post:
        pass

    @abstractmethod
    def find_post_list(self) -> List[Post]:
        pass

    @abstractmethod
    def save(self, post: Post):
        pass

    @abstractmethod
    def delete(self, post_id):
        pass
