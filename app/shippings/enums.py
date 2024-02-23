from django.db import models


class ShipmentStatus(models.IntegerChoices):
    PENDING = 1, 'Pending'
    SHIPPED = 2, 'Shipped'
    DELIVERED = 3, 'Delivered'


class DeliveryStatusStatus(models.IntegerChoices):
    IN_TRANSIT = 1, 'In Transit'
    OUT_FOR_DELIVERY = 2, 'Out for Delivery'
    DELIVERED = 3, 'Delivered'
