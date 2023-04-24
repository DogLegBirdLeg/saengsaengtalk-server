from app.api.History.Domain.RepositoryInterface import HistoryRepository
from app.api.Post.Domain.Entity.Post import Post
from app.api.Order.Domain.Entity.Order import Order
from app.api.Post.util.PostMapper import PostMapper
from app.api.Order.util.Mapper import OrderMapper
from typing import List


class MongoDBHistoryRepository(HistoryRepository):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['delivery']

    def find_post_history_list(self, user_id) -> List[Post]:
        find = {
            'status': {'$in': ['delivered', 'canceled']},
            'users': {'$eq': user_id}
        }
        post_history_list = self.db.post.find(find)
        return [PostMapper.post_mapping(post_history) for post_history in post_history_list]

    def find_order_history_list(self, post_id) -> List[Order]:
        find = {'post_id': post_id}
        orders = self.db.order.find(find)

        return [OrderMapper.order_mapper(order) for order in orders]
