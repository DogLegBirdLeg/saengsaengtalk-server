from abc import *
from typing import List
from logic.delivery.post.domain.entity.Post import Post
from logic.delivery.post.domain.vo.store_vo import StoreVO


class PostDAO(metaclass=ABCMeta):
    @abstractmethod
    def find_joinable_posts_by_user_id(self, user_id) -> List[Post]:
        pass

    @abstractmethod
    def find_joined_posts_by_user_id(self, user_id) -> List[Post]:
        pass

    @abstractmethod
    def find_all_posts_by_user_id(self, user_id) -> List[Post]:
        pass

    @abstractmethod
    def update_status(self, post: Post):
        pass

    @abstractmethod
    def update_content(self, post: Post):
        pass

    @abstractmethod
    def update_users(self, post: Post):
        pass


class StoreDAO(metaclass=ABCMeta):
    @abstractmethod
    def find_store_summary_by_id(self, store_id) -> StoreVO:
        pass
