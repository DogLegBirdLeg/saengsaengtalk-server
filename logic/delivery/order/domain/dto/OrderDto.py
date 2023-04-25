from logic.delivery.order.domain.entity.Order import Order
from logic.delivery.order.domain.entity.OrderLine import OrderLine
from logic.delivery.order.domain.entity.OrderMenu import OrderMenu
from logic.delivery.order.domain.entity.OrderGroup import OrderGroup
from logic.delivery.order.domain.entity.OrderOption import OrderOption
from typing import List


class OrderOptionDto:
    def __init__(self, _id: str, name: str, price: int):
        self._id = _id
        self.name = name
        self.price = price

    @property
    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'price': self.price
        }

    @staticmethod
    def mapping(order_option):
        return OrderOptionDto(_id=order_option._id,
                              name=order_option.name,
                              price=order_option.price)


class OrderGroupDto:
    def __init__(self, _id, name, min_order_quantity, max_order_quantity, order_options: List[OrderOptionDto]):
        self._id = _id
        self.name = name
        self.min_order_quantity = min_order_quantity
        self.max_order_quantity = max_order_quantity
        self.order_options = order_options

    @property
    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'min_order_quantity': self.min_order_quantity,
            'max_order_quantity': self.max_order_quantity,
            'options': [order_option.json for order_option in self.order_options]
        }

    @staticmethod
    def mapping(order_group: OrderGroup):
        return OrderGroupDto(_id=order_group._id,
                             name=order_group.name,
                             min_order_quantity=order_group.min_order_quantity,
                             max_order_quantity=order_group.max_order_quantity,
                             order_options=[OrderOptionDto.mapping(order_option) for order_option in order_group.order_options])


class OrderMenuDto:
    def __init__(self, _id, name, price, order_groups: List[OrderGroupDto]):
        self._id = _id
        self.name = name
        self.price = price
        self.order_groups = order_groups

    @property
    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'price': self.price,
            'groups': [order_group.json for order_group in self.order_groups]
        }

    @staticmethod
    def mapping(order_menu: OrderMenu):
        return OrderMenuDto(_id=order_menu._id,
                            name=order_menu.name,
                            price=order_menu.price,
                            order_groups=[OrderGroupDto.mapping(order_group) for order_group in order_menu.order_groups])


class OrderLineDto:
    def __init__(self, quantity: int, order_menu: OrderMenuDto):
        self.quantity = quantity
        self.order_menu = order_menu

    @property
    def json(self):
        return {
            'quantity': self.quantity,
            'menu': self.order_menu.json
        }

    @staticmethod
    def mapping(order_line: OrderLine):
        return OrderLineDto(quantity=order_line.quantity,
                            order_menu=OrderMenuDto.mapping(order_line.order_menu))


class OrderDto:
    def __init__(self, post_id, user_id, nickname, request_comment, order_lines: List[OrderLineDto]):
        self.post_id = post_id
        self.user_id = user_id
        self.nickname = nickname
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

    @staticmethod
    def mapping(order: Order):
        return OrderDto(post_id=order.post_id,
                        user_id=order.user_id,
                        nickname=order.nickname,
                        request_comment=order.request_comment,
                        order_lines=[OrderLineDto.mapping(order_line) for order_line in order.order_lines])
