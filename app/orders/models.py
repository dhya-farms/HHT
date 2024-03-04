from django.db import models

from app.orders.enums import OrderStatus


class Order(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='orders')
    product_variants = models.ManyToManyField('products.ProductVariant', through='OrderItem')
    coupon = models.ForeignKey("products.Coupon", on_delete=models.CASCADE, related_name='orders', blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    status = models.IntegerField(choices=OrderStatus.choices, default=OrderStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} ({self.status})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey('products.ProductVariant', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at the time of order

    def __str__(self):
        return f"{self.quantity} x {self.product_variant.name} in Order {self.order.id}"
