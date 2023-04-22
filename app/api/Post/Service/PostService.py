from typing import List, Tuple
from app.api.History.Domain.RepositoryInterface import HistoryRepository
from app.api.Post.Domain.RepositoryInterface import PostRepository
from app.api.Order.Domain.RepositoryInterface import OrderRepository
from app.api.Post.Domain.Entity.Post import Post
from app.api.Post.Domain.DomainService.PostFilteringService import PostFilteringService
from app.api.Post.Domain.DomainService.PostCreateService import PostCreateService
from blinker import Namespace
from flask import g

post_ns = Namespace()
post_event = post_ns.signal('post-event')


class PostService:
    def __init__(self,
                 post_repository: PostRepository,
                 history_repository: HistoryRepository,
                 order_repository: OrderRepository,
                 post_create_service: PostCreateService,
                 post_filtering_service: PostFilteringService):
        self.post_repository = post_repository
        self.history_repository = history_repository
        self.order_repository = order_repository
        self.post_create_service = post_create_service
        self.post_filtering_service = post_filtering_service

    def get_list(self, option) -> List[Tuple[Post, List[int]]]:
        posts = self.post_filtering_service.filtering(option, g.id)
        return posts

    def get(self, post_id) -> (Post, List[int]):
        post = self.post_repository.find_post(post_id)
        orders = self.order_repository.find_order_list_by_post_id(post_id)
        return post, [order.user_id for order in orders]

    def create(self, store_id, place, order_time, min_member, max_member, order_json) -> str:
        post = self.post_create_service.create(store_id, place, order_time, min_member, max_member)
        self.post_repository.save(post)

        post_event.send('created', store_id=store_id, post_id=post._id, order_json=order_json)
        return post._id

    def delete(self, post_id):
        post = self.post_repository.find_post(post_id)
        post.can_delete()
        self.post_repository.delete(post._id)
        self.history_repository.save_post(post)

        post_event.send('deleted', post_id=post_id)

    def modify(self, post_id, order_time, place, min_member, max_member):
        post = self.post_repository.find_post(post_id)
        post.modify_content(order_time, place, min_member, max_member)
        self.post_repository.update(post)

    def change_status(self, post_id, status):
        post = self.post_repository.find_post(post_id)
        post.set_status(status)
        self.post_repository.update(post)
        # TODO: status에 따른 분기처리
        if status == 'ordered':
            # push 알림 코드
            pass

        elif status == 'delivered':
            # push 알림 코드

            self.history_repository.save_post(post)
            self.post_repository.delete(post_id)
            post_event.send('deleted', post_id=post_id)
