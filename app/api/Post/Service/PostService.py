from flask import g
from typing import List, Tuple
from bson import ObjectId
from app import exceptions

from app.api.Order.Domain.DomainService.OrderCreateService import OrderCreateService
from app.api.Order.Domain.RepositoryInterface import OrderReader, OrderWriter

from app.api.Post.Domain.RepositoryInterface import PostReader, PostWriter
from app.api.Post.Domain.Entity.Post import Post
from app.api.Post.Domain.DomainService.PostCreateService import PostCreateService
from app.api.Post.Domain.DomainService.PostFilteringService import PostFilteringService

from app.api.History.Domain.RepositoryInterface import HistoryWriter


class PostService:
    def __init__(self,
                 post_reader: PostReader,
                 post_writer: PostWriter,
                 order_reader: OrderReader,
                 order_writer: OrderWriter,
                 history_writer: HistoryWriter,
                 post_filtering_service: PostFilteringService,
                 post_create_service: PostCreateService,
                 order_create_service: OrderCreateService):
        self.post_reader = post_reader
        self.post_writer = post_writer
        self.order_reader = order_reader
        self.order_writer = order_writer
        self.history_writer = history_writer
        self.post_filtering_service = post_filtering_service
        self.post_create_service = post_create_service
        self.order_create_service = order_create_service

    def get_list(self, option) -> List[Tuple[Post, List[int]]]:
        posts = self.post_filtering_service.filtering(option, g.id)
        return posts

    def get(self, post_id) -> (Post, List[int]):
        post = self.post_reader.find_post(post_id)
        orders = self.order_reader.find_order_list_by_post_id(post_id)
        return post, [order.user_id for order in orders]

    def create(self, store_id, place, order_time, min_member, max_member, order_json) -> str:
        post_id = str(ObjectId())

        order = self.order_create_service.create(store_id, post_id, g.id, g.nickname, order_json)
        post = self.post_create_service.create(post_id, store_id, g.id, g.nickname, place, order_time, min_member, max_member, order)
        self.post_writer.set(post)

        return post_id

    def delete(self, post_id):
        post = self.post_reader.find_post(post_id)

        if post.is_owner(g.id) is False:
            raise exceptions.AccessDenied

        if post.is_recruit() is True:
            raise exceptions.ClosedPost

        self.post_writer.delete(post_id)
        self.order_writer.delete_post(post_id)

    def modify(self, post_id, order_time, place, min_member, max_member):
        post = self.post_reader.find_post(post_id)

        if post.is_owner(g.id) is False:
            raise exceptions.AccessDenied

        if post.is_recruit() is True:
            raise exceptions.ClosedPost

        post.modify_content(order_time, place, min_member, max_member)
        self.post_writer.update(post)

    def update_status(self, post_id, filed, status):
        post = self.post_reader.find_post(post_id)

        if post.is_owner(g.id) is False:
            raise exceptions.AccessDenied

        post.update_status(filed, status)
        self.post_writer.update(post)

    def delivered(self, post_id):
        post = self.post_reader.find_post(post_id)
        self.post_writer.delete(post_id)

        orders = self.order_reader.find_order_list_by_post_id(post_id)
        self.order_writer.delete_post(post_id)

        self.history_writer.save(post, orders)
