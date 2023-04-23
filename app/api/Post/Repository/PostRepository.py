from app import exceptions
import json
from typing import List

from app.api.Post.Domain.Entity.Post import Post
from app.api.Post.Domain.RepositoryInterface import PostRepository

from app.api.Post.util.PostMapper import PostMapper


class RedisPostRepository(PostRepository):
    def __init__(self, redis_connection):
        self.db = redis_connection

    def find_post(self, post_id: str) -> Post:
        data = self.db.get(post_id)
        if data is None:
            raise exceptions.NotExistPost

        post_json = json.loads(data)
        return PostMapper.post_mapping(post_json)

    def find_post_list(self) -> List[Post]:
        datas = self.db.mget(self.db.keys())

        post_list = [
            PostMapper.post_mapping(json.loads(data))
            for data in datas
        ]
        return post_list

    def save(self, post: Post):
        self.db.set(post._id, json.dumps(post.json))

    def update(self, post: Post):
        self.db.set(post._id, json.dumps(post.json))

    def delete(self, post_id: str):
        self.db.delete(post_id)


class MongoDBPostRepository(PostRepository):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['delivery']

    def find_post(self, post_id: str) -> Post:
        find = {'_id': post_id}
        post_json = self.db.post.find_one(find)
        if post_json is None:
            raise exceptions.NotExistPost

        return PostMapper.post_mapping(post_json)

    def find_post_list(self) -> List[Post]:
        find = {'$nin': {'status': ['delivered', 'canceled']}}
        posts = self.db.post.find(find)

        return [PostMapper.post_mapping(post.json) for post in posts]

    def save(self, post: Post):
        self.db.post.insert_one(post.json)

    def update(self, post: Post):
        pass

    def delete(self, post_id: str):
        find = {'_id': post_id}
        update = {'status': 'deleted'}
        self.db.post.update(find, update)