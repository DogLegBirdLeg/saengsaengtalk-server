from app.api.Store.Domain.RepositoryInterface import MenuReader
from app.api.Order.Domain.Entity.Order import Order
from app.api.Order.Domain.DomainService.OrderValidator import OrderValidator
from app.api.Order.util.Mapper import OrderMapper


class OrderCreateService:
    def __init__(self, menu_reader: MenuReader, order_validator: OrderValidator):
        self.menu_reader = menu_reader
        self.order_validator = order_validator

    def create(self, store_id, post_id, user_id, nickname, order_json) -> Order:
        order_json['post_id'] = post_id
        order_json['user_id'] = user_id
        order_json['nickname'] = nickname

        order = OrderMapper.order_mapper(order_json)
        menus = self.menu_reader.find_menu_list(store_id)
        self.order_validator.validate_order(menus, order)
        return order

