from flask import g
from typing import List

from app.api.Post.Domain.Entity.Post import Post
from app.api.Order.Domain.Entity.Order import Order
from app.api.History.Domain.RepositoryInterface import HistoryRepository


class HistoryService:
    def __init__(self, history_repository: HistoryRepository):
        self.history_repository = history_repository

    def get_history_list(self) -> List[Post]:
        return self.history_repository.find_post_history_list(g.id)

    def get_order_history(self, post_id) -> List[Order]:
        return self.history_repository.find_order_history_list(post_id)
