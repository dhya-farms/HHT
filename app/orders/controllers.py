from app.orders.models import Order, OrderItem
from app.utils.controllers import Controller


class OrderController(Controller):
    def __init__(self):
        super().__init__(model=Order)


class OrderItemController(Controller):
    def __init__(self):
        super().__init__(model=OrderItem)
