from django.db import models

from app.payments.enums import PaymentMethod, PaymentStatus, RazorpayWebhookEventType, RefundType, ReturnStatus, \
    RefundStatus


class Payment(models.Model):
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.PositiveSmallIntegerField(choices=PaymentMethod.choices)
    payment_status = models.PositiveSmallIntegerField(choices=PaymentStatus.choices)
    transaction_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id}"


class Return(models.Model):
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='returns')
    reason = models.TextField()
    status = models.PositiveSmallIntegerField(choices=ReturnStatus.choices, default=ReturnStatus.REQUESTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Return {self.id} for Order {self.order.id}"


class Refund(models.Model):
    return_obj = models.OneToOneField(Return, on_delete=models.CASCADE, related_name='refund', null=True, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='refunds')
    refund_type = models.PositiveSmallIntegerField(choices=RefundType.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField(blank=True)
    status = models.PositiveSmallIntegerField(choices=RefundStatus.choices)
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.return_obj:
            return f"Refund {self.id} for Return {self.return_obj.id}"
        else:
            return f"Refund {self.id} for Payment {self.payment.id}"


class ReturnItem(models.Model):
    return_obj = models.ForeignKey(Return, on_delete=models.CASCADE, related_name='return_items')
    product_variant = models.ForeignKey('products.ProductVariant', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ReturnItem {self.id} for Return {self.return_order.id}"

# class WebhookEvent(models.Model):
#     event_type = models.PositiveSmallIntegerField(choices=RazorpayWebhookEventType.choices)
#     payload = models.JSONField()
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"WebhookEvent {self.id} - {self.get_event_type_display()}"
