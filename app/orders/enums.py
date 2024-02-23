from django.db import models


class OrderStatus(models.IntegerChoices):
    PENDING = 1, 'Pending'
    CONFIRMED = 2, 'Confirmed'
    SHIPPED = 3, 'Shipped'
    DELIVERED = 4, 'Delivered'
    CANCELED = 5, 'Canceled'
