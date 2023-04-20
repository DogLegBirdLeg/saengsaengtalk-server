from app.api.Order.Domain.Entity.OrderMenu import OrderMenu


class OrderLine:
    def __init__(self, quantity: int, order_menu: OrderMenu):
        self.quantity = quantity
        self.order_menu = order_menu

    @property
    def json(self):
        return {
            'quantity': self.quantity,
            'menu': self.order_menu.json
        }
