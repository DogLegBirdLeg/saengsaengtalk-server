from flask import g
from typing import List
import exceptions

from logic.delivery.order.application.port.incoming.OrderQueryUseCase import OrderQueryUseCase
from logic.delivery.order.application.port.outgoing.persistance.OrderRepository import OrderRepository
from logic.delivery.order.domain.entity.Order import Order


class OrderQueryService(OrderQueryUseCase):
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def get(self, post_id) -> Order:
        try:
            order = self.order_repository.find_order_by_user_id(post_id, g.id)
        except exceptions.NotExistResource:
            raise exceptions.NotJoinedUser

        return order

    def get_list(self, post_id) -> List[Order]:
        orders = self.order_repository.find_all_order_by_post_id(post_id)
        return orders
