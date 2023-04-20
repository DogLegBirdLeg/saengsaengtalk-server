from abc import *
from typing import List

from app.api.Post.Domain.Entity.Post import Post


class PostReader(metaclass=ABCMeta):
    @abstractmethod
    def find_post(self, post_id) -> Post:
        pass

    @abstractmethod
    def find_post_list(self) -> List[Post]:
        pass


class PostWriter(metaclass=ABCMeta):
    @abstractmethod
    def set(self, post: Post):
        pass

    @abstractmethod
    def update(self, post: Post):
        pass

    @abstractmethod
    def delete(self, post_id):
        pass
