from abc import *
from typing import List
from app.api.Post.Domain.Entity.Post import Post
from app.api.Post.util.PostMapper import PostMapper


class PostDAO(metaclass=ABCMeta):
    @abstractmethod
    def find_joinable_posts(self, user_id) -> List[Post]:
        pass

    @abstractmethod
    def find_joined_posts(self, user_id) -> List[Post]:
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


class MongoDBPostDAO(PostDAO):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['delivery']

    def find_joinable_posts(self, user_id) -> List[Post]:
        find = {
            'status': 'recruiting',
            'users': {'$ne': user_id}
        }

        posts_json = self.db.post.find(find)
        return [PostMapper.post_mapping(post_json) for post_json in posts_json]

    def find_joined_posts(self, user_id) -> List[Post]:
        find = {
            'status': {'$nin': ['delivered', 'canceled']},
            'users': {'$eq': user_id}
        }
        posts_json = self.db.post.find(find)
        return [PostMapper.post_mapping(post_json) for post_json in posts_json]

    def update_status(self, post: Post):
        find = {'_id': post._id}
        update = {'$set': {'status': post.status}}
        self.db.post.update_one(find, update)

    def update_content(self, post: Post):
        find = {'_id': post._id}
        update = {
            '$set': {
                'order_time': post.order_time,
                'place': post.place,
                'min_member': post.min_member,
                'max_member': post.max_member
            }
        }
        self.db.post.update_one(find, update)

    def update_users(self, post: Post):
        find = {'_id': post._id}
        update = {'$set': {'users': post.users}}

        self.db.post.update_one(find, update)
