from rest_framework import serializers

from app.orders.serializers import OrderSerializer
from app.payments.enums import PaymentMethod, PaymentStatus, RefundType, ReturnStatus, RefundStatus
from app.payments.models import Payment, Return, Refund, ReturnItem
from app.products.serializers import ProductVariantSerializer
from app.utils.helpers import get_serialized_enum


class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    payment_method = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()

    def get_payment_method(self, obj):
        return get_serialized_enum(PaymentMethod(obj.payment_method))

    def get_payment_status(self, obj):
        return get_serialized_enum(PaymentStatus(obj.payment_method))

    class Meta:
        model = Payment
        fields = '__all__'


class ReturnSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return get_serialized_enum(ReturnStatus(obj.status))

    class Meta:
        model = Return
        fields = '__all__'


class RefundSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    return_obj = ReturnSerializer(read_only=True)
    refund_type = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_refund_type(self, obj):
        return get_serialized_enum(RefundType(obj.refund_type))

    def get_status(self, obj):
        return get_serialized_enum(RefundStatus(obj.status))

    class Meta:
        model = Refund
        fields = '__all__'


class ReturnItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)
    return_order = ReturnSerializer(read_only=True)

    class Meta:
        model = ReturnItem
        fields = '__all__'
