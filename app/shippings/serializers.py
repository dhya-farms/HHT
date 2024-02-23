from rest_framework import serializers
from .models import ShippingProvider, Shipment, DeliveryStatus
from .enums import ShipmentStatus, DeliveryStatusStatus
from ..utils.helpers import get_serialized_enum


class ShippingProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingProvider
        fields = '__all__'


class ShipmentSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return get_serialized_enum(ShipmentStatus(obj.status))

    class Meta:
        model = Shipment
        fields = '__all__'
        read_only_fields = ['status_display']


class DeliveryStatusSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return get_serialized_enum(DeliveryStatusStatus(obj.status))

    class Meta:
        model = DeliveryStatus
        fields = '__all__'
        read_only_fields = ['status_display']
