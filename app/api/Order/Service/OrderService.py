from flask import g
from typing import List
from app import exceptions

from app.api.Order.Domain.DomainService.OrderCreateService import OrderCreateService
from app.api.Order.Domain.RepositoryInterface import OrderReader, OrderWriter
from app.api.Order.Domain.Entity.Order import Order

from app.api.Post.Domain.RepositoryInterface import PostReader


class OrderService:
    def __init__(self,
                 order_reader: OrderReader,
                 order_writer: OrderWriter,
                 post_reader: PostReader,
                 order_create_service: OrderCreateService):

        self.order_reader = order_reader
        self.order_writer = order_writer
        self.post_reader = post_reader
        self.order_create_service = order_create_service

    def get(self, post_id) -> Order:
        try:
            order = self.order_reader.find_order_by_user_id(post_id, g.id)
        except exceptions.NotExistResource:
            raise exceptions.NotJoinedUser
        return order

    def get_list(self, post_id) -> List[Order]:
        orders = self.order_reader.find_order_list_by_post_id(post_id)
        return orders

    def join(self, post_id, order_json):
        post = self.post_reader.find_post(post_id)

        orders = self.order_reader.find_order_list_by_post_id(post_id)

        join_user_id = [order.user_id for order in orders]
        if g.id in join_user_id:
            raise exceptions.AlreadyJoinedUser

        order = self.order_create_service.create(post.store._id, post_id, g.id, g.nickname, order_json)
        self.order_writer.save(order.post_id, order)

    def quit(self, post_id):
        post = self.post_reader.find_post(post_id)
        orders = self.order_reader.find_order_list_by_post_id(post_id)

        if post.is_owner(g.id):
            raise exceptions.OwnerQuit

        if post.is_recruit():
            raise exceptions.ClosedPost

        join_user_id = [order.user_id for order in orders]
        if g.id not in join_user_id:
            raise exceptions.NotJoinedUser

        self.order_writer.delete(post_id, g.id)
