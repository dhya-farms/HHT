from app.shippings.models import ShippingProvider, Shipment, DeliveryStatus
from app.utils.controllers import Controller


class ShippingProviderController(Controller):
    def __init__(self):
        super().__init__(model=ShippingProvider)


class ShipmentController(Controller):
    def __init__(self):
        super().__init__(model=Shipment)


class DeliveryStatusController(Controller):
    def __init__(self):
        super().__init__(model=DeliveryStatus)
