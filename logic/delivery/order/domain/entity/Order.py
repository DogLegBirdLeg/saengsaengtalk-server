from typing import List
from logic.delivery.order.domain.entity.OrderLine import OrderLine


class Order:
    def __init__(self, post_id, user_id, nickname, request_comment, order_lines: List[OrderLine]):
        self.post_id = post_id
        self.user_id = user_id
        self.nickname = nickname
        self.request_comment = request_comment
        self.order_lines = order_lines

