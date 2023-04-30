from app import exceptions

from logic.delivery.post.util.PostMapper import PostMapper
from logic.delivery.post.domain.entity.Post import Post
from logic.delivery.post.domain.RepositoryInterface import IPostRepository


class MongoDBPostRepository(IPostRepository):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['delivery']

    def find_post_by_id(self, post_id: str) -> Post:
        find = {'_id': post_id}
        post_json = self.db.post.find_one(find)
        if post_json is None:
            raise exceptions.NotExistPost

        return PostMapper.post_mapping(post_json)

    def save(self, post: Post):
        data = {
            '_id': post._id,
            'title': post.title,
            'store': {
                '_id': post.store._id,
                'name': post.store.name,
                'fee': post.store.fee,
                'min_order': post.store.min_order,
                'note': post.store.note
            },
            'user_id': post.user_id,
            'nickname': post.nickname,
            'status': post.status,
            'place': post.place,
            'order_time': post.order_time,
            'min_member': post.min_member,
            'max_member': post.max_member,
            'users': post.users
        }
        self.db.post.insert_one(data)

    def delete(self, post_id: str):
        find = {'_id': post_id}
        update = {'$set': {'status': 'canceled'}}
        self.db.post.update_one(find, update)
