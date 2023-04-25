from logic.delivery.store.domain.entity.Menu import Menu
from logic.delivery.store.domain.entity.Group import Group
from logic.delivery.store.domain.entity.Option import Option
from logic.delivery.order.domain.entity.OrderMenu import OrderMenu
from logic.delivery.order.domain.entity.OrderGroup import OrderGroup
from logic.delivery.order.domain.entity.OrderOption import OrderOption
from logic.delivery.order.domain.entity.Order import Order
from typing import List
from app import exceptions


class OrderValidator:
    def validate_order(self, menus: List[Menu], order: Order):
        for order_line in order.order_lines:
            self._validate_menu(order_line.order_menu, menus)

    def _validate_menu(self, order_menu: OrderMenu, menus: List[Menu]):
        def find_menu(_id):
            for menu in menus:
                if menu._id == _id:
                    return menu

        menu = find_menu(order_menu._id)
        if menu is None:
            raise exceptions.NotValidOrder

        if order_menu.name != menu.name:
            raise exceptions.NotValidOrder

        if order_menu.price != menu.price:
            raise exceptions.NotValidOrder

        for order_group in order_menu.order_groups:
            self._validate_group(order_group, menu.groups)

    def _validate_group(self, order_group: OrderGroup, groups: List[Group]):
        def find_group(_id):
            for group in groups:
                if group._id == _id:
                    return group

        group = find_group(order_group._id)
        if group is None:
            raise exceptions.NotValidOrder

        if order_group.name != group.name:
            raise exceptions.NotValidOrder

        if order_group.min_order_quantity != group.min_order_quantity:
            raise exceptions.NotValidOrder

        if order_group.max_order_quantity != group.max_order_quantity:
            raise exceptions.NotValidOrder

        for order_option in order_group.order_options:
            self._validate_option(order_option, group.options)

    def _validate_option(self, order_option: OrderOption, options: List[Option]):
        def find_option(_id):
            for option in options:
                if option._id == _id:
                    return option

        option = find_option(order_option._id)
        if option is None:
            raise exceptions.NotValidOrder

        if option.name != order_option.name:
            raise exceptions.NotValidOrder

        if option.price != order_option.price:
            raise exceptions.NotValidOrder