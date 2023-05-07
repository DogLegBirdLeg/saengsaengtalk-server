from logic.delivery.post.domain.entity.Post import Post
from logic.delivery.post.application.port.outgoing.persistence.PostUpdateDao import PostUpdateDao
from bson import ObjectId

class MongoDBPostUpdateDao(PostUpdateDao):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['delivery']

    def update_status(self, post: Post):
        find = {'_id': ObjectId(post._id)}
        update = {'$set': {'status': post.status}}
        self.db.post.update_one(find, update)

    def update_content(self, post: Post):
        find = {'_id': ObjectId(post._id)}
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
        find = {'_id': ObjectId(post._id)}
        update = {'$set': {'users': post.users}}

        self.db.post.update_one(find, update)

    def update_fee(self, post: Post):
        find = {'_id': ObjectId(post._id)}
        update = {'$set': {'fee': post.fee}}

        self.db.post.update_one(find, update)
