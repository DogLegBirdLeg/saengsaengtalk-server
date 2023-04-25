from logic.delivery.order.domain.entity.OrderMenu import OrderMenu


class OrderLine:
    def __init__(self, quantity: int, order_menu: OrderMenu):
        self.quantity = quantity
        self.order_menu = order_menu
