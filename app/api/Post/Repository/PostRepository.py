from app import exceptions
from typing import List

from app.api.Post.Domain.Entity.Post import Post
from app.api.Post.Domain.RepositoryInterface import PostRepository

from app.api.Post.util.PostMapper import PostMapper


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
        find = {'status': {'$nin': ['delivered', 'canceled']}}
        posts = self.db.post.find(find)
        return [PostMapper.post_mapping(post_json) for post_json in posts]

    def save(self, post: Post):
        self.db.post.insert_one(post.json)

    def delete(self, post_id: str):
        find = {'_id': post_id}
        update = {'$set': {'status': 'canceled'}}
        self.db.post.update_one(find, update)
