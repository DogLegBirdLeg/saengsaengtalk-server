from typing import List
from bson import ObjectId
import pymongo

from logic.delivery.post.dto.persistance import Post
from logic.delivery.post.application.port.outgoing.persistence.PostQueryDao import PostQueryDao
from datetime import datetime, timedelta
import exceptions


class MongoDBPostQueryDao(PostQueryDao):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['delivery']

    def find_joinable_posts_by_user_id(self, user_id) -> List[Post]:
        find = {
            'order_time': {'$gte': datetime.now()},
            'status': 'recruiting',
            'users': {'$ne': user_id}
        }

        posts_json = self.db.post.find(find).sort("order_time", pymongo.ASCENDING)
        return [Post.mapping(post_json) for post_json in posts_json]

    def find_joined_posts_by_user_id(self, user_id) -> List[Post]:
        find = {
            'status': {'$in': ['recruiting', 'closed', 'ordered']},
            'users': {'$eq': user_id}
        }

        posts_json = self.db.post.find(find).sort("order_time", pymongo.ASCENDING)
        return [Post.mapping(post_json) for post_json in posts_json]

    def find_all_posts_by_user_id(self, user_id) -> List[Post]:
        find = {
            'users': {'$eq': user_id},
            'status': {'$in': ['delivered', 'canceled']}
        }
        posts_json = self.db.post.find(find).sort("order_time", pymongo.ASCENDING)

        return [Post.mapping(post_json) for post_json in posts_json]

    def find_post_by_id(self, post_id) -> Post:
        find = {'_id': ObjectId(post_id)}
        post_json = self.db.post.find_one(find)

        if post_json is None:
            raise exceptions.NotExistPost

        return Post.mapping(post_json)
