from app import exceptions
from typing import List

from logic.delivery.order.domain.entity.Order import Order
from logic.delivery.order.util.Mapper import OrderMapper
from logic.delivery.order.domain.RepositoryInterface import OrderRepository
from logic.delivery.order.domain.dto.OrderDto import OrderDto


class MongoDBOrderRepository(OrderRepository):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['delivery']

    def find_order_by_user_id(self, post_id, user_id) -> Order:
        find = {
            '$and': [
                {'post_id': post_id},
                {'user_id': user_id}
            ]
        }
        order_json = self.db.order.find_one(find)
        if order_json is None:
            raise exceptions.NotJoinedUser

        return OrderMapper.order_mapper(order_json)

    def find_all_order_by_post_id(self, post_id) -> List[Order]:
        find = {'post_id': post_id}
        orders_json = self.db.order.find(find)

        orders = [OrderMapper.order_mapper(order_json) for order_json in orders_json]
        return orders

    def save(self, order: Order):
        order_dto = OrderDto.mapping(order)
        self.db.order.insert_one(order_dto.json)

    def delete(self, post_id: str, user_id: str):
        find = {'post_id': post_id, 'user_id': user_id}
        self.db.order.delete_one(find)
