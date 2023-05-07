from app import exceptions
from bson import ObjectId
from logic.delivery.post.util.PostMapper import PostMapper
from logic.delivery.post.domain.entity.Post import Post
from logic.delivery.post.application.port.outgoing.persistence.PostRepository import PostRepository


class MongoDBPostRepository(PostRepository):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['delivery']

    def find_post_by_id(self, post_id: str) -> Post:
        find = {'_id': ObjectId(post_id)}
        post_json = self.db.post.find_one(find)
        if post_json is None:
            raise exceptions.NotExistPost

        return PostMapper.post_mapping(post_json)

    def save(self, post: Post):
        find = {'_id': ObjectId(post.store_id)}
        store_json = self.db.store.find_one(find)

        data = {
            '_id': ObjectId(post._id),
            'store': {
                '_id': store_json['_id'],
                'name': store_json['name'],
                'fee': store_json['fee'],
                'min_order': store_json['min_order'],
                'phone_number': store_json['phone_number'],
                'logo_img_url': store_json['logo_img_url'],
                'note': store_json['note']
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
        find = {'_id': ObjectId(post_id)}
        update = {'$set': {'status': 'canceled'}}
        self.db.post.update_one(find, update)
