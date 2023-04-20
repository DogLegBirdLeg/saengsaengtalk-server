from flask import g
from typing import List

from app.api.Post.Domain.Entity.Post import Post
from app.api.Order.Domain.Entity.Order import Order
from app.api.History.Domain.RepositoryInterface import HistoryReader


class HistoryService:
    def __init__(self, history_reader: HistoryReader):
        self.history_reader = history_reader

    def get_history_list(self) -> List[Post]:
        return self.history_reader.find_post_history_list(g.id)

    def get_order_history(self, post_id) -> List[Order]:
        return self.history_reader.find_order_history_list(post_id)
