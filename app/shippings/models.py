from django.db import models
from django.utils.translation import gettext_lazy as _

from app.shippings.enums import ShipmentStatus, DeliveryStatusStatus


class ShippingProvider(models.Model):
    name = models.CharField(max_length=255)
    tracking_url_template = models.URLField(max_length=1024, blank=True, null=True)
    api_endpoint = models.URLField(max_length=1024, blank=True, null=True)
    api_key = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Shipment(models.Model):
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='shipment')
    provider = models.ForeignKey(ShippingProvider, on_delete=models.SET_NULL, null=True, related_name='shipments')
    tracking_number = models.CharField(max_length=255, blank=True, null=True)
    shipped_date = models.DateTimeField(blank=True, null=True)
    estimated_delivery_date = models.DateTimeField(blank=True, null=True)
    actual_delivery_date = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=ShipmentStatus.choices, default=ShipmentStatus.PENDING)

    def __str__(self):
        return f"Shipment {self.id} for Order {self.order.id}"


class DeliveryStatus(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='delivery_statuses')
    status = models.IntegerField(choices=DeliveryStatusStatus.choices, default=DeliveryStatusStatus.IN_TRANSIT)
    status_date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Status {DeliveryStatusStatus(self.status).label} for Shipment {self.shipment.id} on {self.status_date}"
