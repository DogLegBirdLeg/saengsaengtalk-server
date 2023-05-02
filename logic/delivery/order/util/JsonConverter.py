from logic.delivery.order.domain.entity.Order import Order
from logic.delivery.order.domain.entity.OrderLine import OrderLine
from logic.delivery.order.domain.entity.OrderMenu import OrderMenu
from logic.delivery.order.domain.entity.OrderGroup import OrderGroup
from logic.delivery.order.domain.entity.OrderOption import OrderOption


def order_to_json(order: Order):
    return {
        'post_id': order.post_id,
        'user_id': order.user_id,
        'nickname': order.nickname,
        'request_comment': order.request_comment,
        'order_lines': [order_line_to_json(order_line) for order_line in order.order_lines]
    }


def order_line_to_json(order_line: OrderLine):
    return {
        'quantity': order_line.quantity,
        'menu': order_menu_to_json(order_line.order_menu)
    }


def order_menu_to_json(order_menu: OrderMenu):
    return {
        '_id': order_menu._id,
        'name': order_menu.name,
        'price': order_menu.price,
        'groups': [order_group_to_json(order_group) for order_group in order_menu.order_groups]
    }


def order_group_to_json(order_group: OrderGroup):
    return {
        '_id': order_group._id,
        'name': order_group.name,
        'min_order_quantity': order_group.min_order_quantity,
        'max_order_quantity': order_group.max_order_quantity,
        'options': [order_option_to_json(order_option) for order_option in order_group.order_options]
    }


def order_option_to_json(order_option: OrderOption):
    return {
        '_id': order_option._id,
        'name': order_option.name,
        'price': order_option.price
    }
