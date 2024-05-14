from rest_framework import serializers

from .enums import OrderStatus
from .models import Order, OrderItem
from app.customers.serializers import CustomerSerializer  # Assuming you have a CustomerSerializer
from app.products.serializers import CouponSerializer, ProductVariantSerializer  # Assuming these serializers exist
from ..users.serializers import UserSerializer
from ..utils.helpers import get_serialized_enum


class OrderItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    coupon = CouponSerializer(read_only=True)
    status = serializers.SerializerMethodField()
    order_items = OrderItemSerializer(many=True, read_only=True, source='items')  # Include this line

    def get_status(self, obj):
        return get_serialized_enum(OrderStatus(obj.status))

    class Meta:
        model = Order
        fields = '__all__'
