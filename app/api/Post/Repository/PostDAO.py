from abc import *
from typing import List
from app.api.Post.Domain.Entity.Post import Post


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


class MongoDBPostDAO(PostDAO):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['delivery']

    def find_joinable_posts(self, user_id) -> List[Post]:
        '''status : recruiting'''
        pipe1 = {
            '$lookup': {
                'from': 'post',
                'localField': 'post_id',
                'foreignField': '_id',
                'as': 'post'
            }
        }
        pipe1 = {'$match': {'status': 'recruiting'}}


    def find_joined_posts(self, user_id) -> List[Post]:
        '''status : delivered, canceled 빼고'''
        pass

    def update_status(self, post: Post):
        find = {'_id': post._id}
        update = {'status': post.status}
        self.db.post.update(find, update)

    def update_content(self, post: Post):
        find = {'_id': post._id}
        update = {
            'order_time': post.order_time,
            'place': post.place,
            'min_member': post.min_member,
            'max_member': post.max_member
        }
        self.db.post.update(find, update)