from flask import g
from typing import List
from app import exceptions

from app.api.Order.Domain.DomainService.OrderCreateService import OrderCreateService
from app.api.Order.Domain.RepositoryInterface import OrderRepository
from app.api.Post.Domain.RepositoryInterface import PostRepository
from app.api.Order.Domain.Entity.Order import Order


class OrderService:
    def __init__(self,
                 order_repository: OrderRepository,
                 post_repository: PostRepository,
                 order_create_service: OrderCreateService):
        self.order_repository = order_repository
        self.post_repository = post_repository
        self.order_create_service = order_create_service

    def get(self, post_id) -> Order:
        try:
            order = self.order_repository.find_order_by_user_id(post_id, g.id)
        except exceptions.NotExistResource:
            raise exceptions.NotJoinedUser
        return order

    def get_list(self, post_id) -> List[Order]:
        orders = self.order_repository.find_orders_by_post_id(post_id)
        return orders

    def join(self, post_id, order_json):
        post = self.post_repository.find_post(post_id)
        if post.status != 'recruiting':
            raise Exception

        order = self.order_create_service.create(post.store._id, post_id, order_json)
        self.order_repository.save(order)

    def quit(self, post_id):
        post = self.post_repository.find_post(post_id)
        if post.status != 'recruiting':
            raise Exception

        if post.user_id == g.id:
            raise exceptions.OwnerQuit

        self.order_repository.delete(post_id, g.id)
