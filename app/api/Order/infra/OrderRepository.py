from app import exceptions
from typing import List

from app.api.Order.Domain.Entity.Order import Order
from app.api.Order.util.Mapper import OrderMapper
from app.api.Order.Domain.RepositoryInterface import OrderRepository


class MongoDBOrderRepository(OrderRepository):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['delivery']

    def find_order_by_user_id(self, post_id, user_id) -> Order:
        find = {'post_id': post_id, 'user_id': user_id}
        order_json = self.db.order.find_one(find)
        if order_json is None:
            raise exceptions.NotJoinedUser

        return OrderMapper.order_mapper(order_json)

    def find_orders_by_post_id(self, post_id) -> List[Order]:
        find = {'post_id': post_id}
        orders_json = self.db.order.find(find)

        orders = [OrderMapper.order_mapper(order_json) for order_json in orders_json]
        return orders

    def save(self, order: Order):
        self.db.order.insert_one(order.json)

    def delete(self, post_id: str, user_id: str):
        find = {'post_id': post_id, 'user_id': user_id}
        self.db.order.delete(find)
