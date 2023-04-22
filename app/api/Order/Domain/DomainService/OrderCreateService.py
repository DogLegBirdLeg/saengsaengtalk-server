from app.api.Store.Domain.RepositoryInterface import MenuRepository
from app.api.Order.Domain.Entity.Order import Order
from app.api.Order.Domain.DomainService.OrderValidator import OrderValidator
from app.api.Order.util.Mapper import OrderMapper
from flask import g


class OrderCreateService:
    def __init__(self, menu_repository: MenuRepository, order_validator: OrderValidator):
        self.menu_repository = menu_repository
        self.order_validator = order_validator

    def create(self, store_id, post_id, order_json) -> Order:
        order_json['post_id'] = post_id
        order_json['user_id'] = g.id
        order_json['nickname'] = g.nickname

        order = OrderMapper.order_mapper(order_json)
        menus = self.menu_repository.find_menu_list(store_id)
        self.order_validator.validate_order(menus, order)
        return order

