from app.api.History.Domain.RepositoryInterface import HistoryReader, HistoryWriter
from app.api.Post.Domain.Entity.Post import Post
from app.api.Order.Domain.Entity.Order import Order
from app.api.Post.util.PostMapper import PostMapper
from app.api.Order.util.Mapper import OrderMapper
from typing import List


class MongoDBHistoryRepository(HistoryReader, HistoryWriter):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['delivery']

    def find_post_history_list(self, user_id) -> List[Post]:
        find = {'orders.user_id': user_id}
        projection = {'orders': False}
        post_history_list = self.db.post.find(find, projection)
        return [PostMapper.post_mapping(post_history) for post_history in post_history_list]

    def find_order_history_list(self, post_id) -> List[Order]:
        find = {'_id': post_id}
        orders = self.db.post.find_one(find)['orders']
        return [OrderMapper.order_mapper(post_id, order['user_id'], order['nickname'], order['order_lines']) for order in orders]

    def save(self, post: Post, orders: List[Order]):
        post_json = post.json
        post_json['orders'] = [order.json for order in orders]
        self.db.post.insert_one(post_json)
