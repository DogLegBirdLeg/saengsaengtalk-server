from typing import List
from logic.delivery.post.domain.entity.Post import Post
from logic.delivery.post.application.IDao import IPostDAO
from logic.delivery.post.util.PostMapper import PostMapper


class MongoDBPostDAO(IPostDAO):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['delivery']

    def find_joinable_posts_by_user_id(self, user_id) -> List[Post]:
        find = {
            'status': 'recruiting',
            'users': {'$ne': user_id}
        }

        posts_json = self.db.post.find(find)
        return [PostMapper.post_mapping(post_json) for post_json in posts_json]

    def find_joined_posts_by_user_id(self, user_id) -> List[Post]:
        find = {
            'status': {'$nin': ['delivered', 'canceled']},
            'users': {'$eq': user_id}
        }
        posts_json = self.db.post.find(find)
        return [PostMapper.post_mapping(post_json) for post_json in posts_json]

    def find_all_posts_by_user_id(self, user_id) -> List[Post]:
        find = {'users': {'$eq': user_id}}
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
