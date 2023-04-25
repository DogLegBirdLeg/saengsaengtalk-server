from logic.delivery.order.domain.entity.Order import Order
from logic.delivery.order.domain.entity.OrderLine import OrderLine
from logic.delivery.order.domain.entity.OrderMenu import OrderMenu
from logic.delivery.order.domain.entity.OrderGroup import OrderGroup
from logic.delivery.order.domain.entity.OrderOption import OrderOption


class OrderMapper:
    @staticmethod
    def order_mapper(order_json) -> Order:
        order = Order(order_json['post_id'],
                      order_json['user_id'],
                      order_json['nickname'],
                      order_json['request_comment'],
                      [OrderMapper.order_line_mapping(order_line_json) for order_line_json in order_json['order_lines']])

        return order

    @staticmethod
    def order_line_mapping(order_line_json) -> OrderLine:
        order = OrderLine(order_line_json['quantity'],
                          OrderMenuMapper.order_menu_mapping(order_line_json['menu']))
        return order


class OrderMenuMapper:
    @staticmethod
    def order_menu_mapping(order_menu_json):
        order_menu = OrderMenu(order_menu_json['_id'],
                               order_menu_json['name'],
                               order_menu_json['price'],
                               [OrderGroupMapper.order_group_mapping(order_group_json) for order_group_json in order_menu_json['groups']])

        return order_menu


class OrderGroupMapper:
    @staticmethod
    def order_group_mapping(order_group_json) -> OrderGroup:
        order_group = OrderGroup(order_group_json['_id'],
                                 order_group_json['name'],
                                 order_group_json['min_order_quantity'],
                                 order_group_json['max_order_quantity'],
                                 [OrderOptionMapper.order_option_mapping(order_option_json) for order_option_json in order_group_json['options']])

        return order_group


class OrderOptionMapper:
    @staticmethod
    def order_option_mapping(order_option_json) -> OrderOption:
        order_option = OrderOption(order_option_json['_id'],
                                   order_option_json['name'],
                                   order_option_json['price'])

        return order_option
