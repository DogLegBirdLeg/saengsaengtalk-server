from typing import List
from logic.delivery.post.dto.persistance import Post
from logic.delivery.post.application.port.outgoing.persistence.PostQueryDao import PostQueryDao
from datetime import datetime, timedelta
from app import exceptions


class MongoDBPostQueryDao(PostQueryDao):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['delivery']

    def find_joinable_posts_by_user_id(self, user_id) -> List[Post]:
        find = {
            'order_time': {'$gte': datetime.now()},
            'status': 'recruiting',
            'users': {'$ne': user_id}
        }

        posts_json = self.db.post.find(find)
        return [Post.mapping(post_json) for post_json in posts_json]

    def find_joined_posts_by_user_id(self, user_id) -> List[Post]:
        current_time = datetime.now()
        one_day_ago = current_time - timedelta(days=1)
        one_day_later = current_time + timedelta(days=1)

        find = {
            'order_time': {'$gte': one_day_ago, '$lte': one_day_later},
            'status': {'$in': ['recruiting', 'closed', 'ordered', 'delivered']},
            'users': {'$eq': user_id}
        }

        posts_json = self.db.post.find(find)
        return [Post.mapping(post_json) for post_json in posts_json]

    def find_all_posts_by_user_id(self, user_id) -> List[Post]:
        find = {'users': {'$eq': user_id}}
        posts_json = self.db.post.find(find)

        return [Post.mapping(post_json) for post_json in posts_json]

    def find_post_by_id(self, post_id) -> Post:
        find = {'_id': post_id}
        post_json = self.db.post.find_one(find)

        if post_json is None:
            raise exceptions.NotExistPost

        return Post.mapping(post_json)
