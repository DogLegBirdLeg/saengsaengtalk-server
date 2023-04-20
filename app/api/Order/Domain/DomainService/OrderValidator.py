from app.api.Store.Domain.Model.Menu import Menus
from app.api.Store.Domain.Model.Group import Groups
from app.api.Store.Domain.Model.Option import Options
from app.api.Order.Domain.Entity.OrderMenu import OrderMenu
from app.api.Order.Domain.Entity.OrderGroup import OrderGroup
from app.api.Order.Domain.Entity.OrderOption import OrderOption
from app.api.Order.Domain.Entity.Order import Order


class OrderValidator:
    def validate_order(self, menus: Menus, order: Order):
        for order_line in order.order_lines:
            self._validate_menu(order_line.order_menu, menus)

    def _validate_menu(self, order_menu: OrderMenu, menus: Menus):
        menu = menus[order_menu._id]
        if menu is None:
            raise Exception

        if order_menu.name != menu.name:
            raise Exception

        if order_menu.price != menu.price:
            raise Exception

        for order_group in order_menu.order_groups:
            self._validate_group(order_group, menu.groups)

    def _validate_group(self, order_group: OrderGroup, groups: Groups):
        group = groups[order_group._id]
        if group is None:
            raise Exception

        if order_group.name != group.name:
            raise Exception

        if order_group.min_order_quantity != group.min_order_quantity:
            raise Exception

        if order_group.max_order_quantity != group.max_order_quantity:
            raise Exception

        for order_option in order_group.order_options:
            self._validate_option(order_option, group.options)

    def _validate_option(self, order_option: OrderOption, options: Options):
        option = options[order_option._id]
        if option is None:
            raise Exception

        if option.name != order_option.name:
            raise Exception

        if option.price != order_option.price:
            raise Exception