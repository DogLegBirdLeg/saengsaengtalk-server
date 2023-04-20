from app import exceptions
import json
from typing import List

from app.api.Post.Domain.Entity.Post import Post
from app.api.Post.Domain.RepositoryInterface import PostReader, PostWriter

from app.api.Post.util.PostMapper import PostMapper


class RedisPostRepository(PostReader, PostWriter):
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

    def set(self, post: Post):
        self.db.set(post._id, json.dumps(post.json))

    def update(self, post: Post):
        self.db.set(post._id, json.dumps(post.json))

    def delete(self, post_id: str):
        self.db.delete(post_id)

