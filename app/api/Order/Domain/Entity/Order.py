from typing import List
from app.api.Order.Domain.Entity.OrderLine import OrderLine
from flask import g


class Order:
    def __init__(self, post_id, request_comment, order_lines: List[OrderLine]):
        self.post_id = post_id
        self.user_id = g.id
        self.nickname = g.id
        self.request_comment = request_comment
        self.order_lines = order_lines

    @property
    def json(self):
        return {
            'post_id': self.post_id,
            'user_id': self.user_id,
            'nickname': self.nickname,
            'request_comment': self.request_comment,
            'order_lines': [order_line.json for order_line in self.order_lines]
        }
