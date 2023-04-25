from logic.delivery.store.domain.RepositoryInterface import MenuRepository
from logic.delivery.order.domain.entity.Order import Order
from logic.delivery.order.domain.domain_service.OrderValidator import OrderValidator
from logic.delivery.order.util.Mapper import OrderMapper


class OrderCreateService:
    def __init__(self, menu_repository: MenuRepository, order_validator: OrderValidator):
        self.menu_repository = menu_repository
        self.order_validator = order_validator

    def create(self, store_id, post_id, user_id, nickname, order_json) -> Order:
        order_json['post_id'] = post_id
        order_json['user_id'] = user_id
        order_json['nickname'] = nickname

        order = OrderMapper.order_mapper(order_json)
        menus = self.menu_repository.find_all_menu_by_store_id(store_id)
        self.order_validator.validate_order(menus, order)
        return order

