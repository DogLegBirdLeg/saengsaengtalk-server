from flask import g
from typing import List
from app import exceptions

from logic.delivery.order.domain.RepositoryInterface import OrderRepository
from logic.delivery.order.domain.dto.OrderDto import OrderDto


class OrderUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def get(self, post_id) -> OrderDto:
        try:
            order = self.order_repository.find_order_by_user_id(post_id, g.id)
        except exceptions.NotExistResource:
            raise exceptions.NotJoinedUser
        return OrderDto.mapping(order)

    def get_list(self, post_id) -> List[OrderDto]:
        orders = self.order_repository.find_all_order_by_post_id(post_id)
        return [OrderDto.mapping(order) for order in orders]
