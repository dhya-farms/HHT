from rest_framework import serializers

from .enums import OrderStatus
from .models import Order, OrderItem
from app.customers.serializers import CustomerSerializer  # Assuming you have a CustomerSerializer
from app.products.serializers import CouponSerializer, ProductVariantSerializer  # Assuming these serializers exist
from ..utils.helpers import get_serialized_enum


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    coupon = CouponSerializer(read_only=True)
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return get_serialized_enum(OrderStatus(obj.status))

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    product_variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'
