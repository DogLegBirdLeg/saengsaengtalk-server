from app import exceptions
import json
from redis import Redis
from typing import List

from app.api.Order.Domain.Entity.Order import Order
from app.api.Order.util.Mapper import OrderMapper
from app.api.Order.Domain.RepositoryInterface import OrderReader, OrderWriter


class RedisOrderRepository(OrderReader, OrderWriter):
    def __init__(self, redis_connection: Redis):
        self.db = redis_connection

    def find_order_by_user_id(self, post_id, user_id) -> Order:
        data = self.db.hget(post_id, user_id)
        if not data:
            raise exceptions.NotExistResource

        order_json = json.loads(data)
        order = OrderMapper.order_mapper(order_json)

        return order

    def find_order_list_by_post_id(self, post_id) -> List[Order]:
        keys = self.db.hkeys(post_id)
        if not keys:
            raise exceptions.NotExistPost

        orders_json = [json.loads(self.db.hget(post_id, key)) for key in keys]

        orders = [OrderMapper.order_mapper(order_json) for order_json in orders_json]
        return orders

    def find_post_join_user(self):
        pipe = self.db.pipeline()

        post_join_user = {}
        keys = self.db.keys()
        for key in keys:
            pipe.hkeys(key)

        posts = pipe.execute()
        for i, key in enumerate(keys):
            post_join_user[key] = posts[i]

        return post_join_user

    def save(self, post_id, order: Order):
        self.db.hset(post_id, order.user_id, json.dumps(order.json))

    def delete(self, post_id: str, user_id: str):
        self.db.hdel(post_id, user_id)

    def delete_post(self, post_id):
        self.db.delete(post_id)
