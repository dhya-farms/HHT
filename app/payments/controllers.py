from app.payments.models import Payment, Return, Refund, ReturnItem
from app.utils.controllers import Controller


class PaymentController(Controller):
    def __init__(self):
        super().__init__(model=Payment)


class ReturnController(Controller):
    def __init__(self):
        super().__init__(model=Return)


class RefundController(Controller):
    def __init__(self):
        super().__init__(model=Refund)


class ReturnItemController(Controller):
    def __init__(self):
        super().__init__(model=ReturnItem)
