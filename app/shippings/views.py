from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .controllers import ShippingProviderController, ShipmentController, DeliveryStatusController
from .models import PincodeAvailability, ShippingRate
from .schemas import ShippingProviderCreateSchema, ShippingProviderUpdateSchema, ShippingProviderListSchema, \
    ShipmentCreateSchema, ShipmentUpdateSchema, ShipmentListSchema, DeliveryStatusCreateSchema, \
    DeliveryStatusUpdateSchema, DeliveryStatusListSchema
from .serializers import ShippingProviderSerializer, ShipmentSerializer, DeliveryStatusSerializer
from ..utils.constants import CacheKeys
from ..utils.views import BaseViewSet


class CheckPincodeAvailability(APIView):
    def get(self, request, pincode):
        try:
            availability = PincodeAvailability.objects.get(pincode=pincode)
            return Response({'pincode': pincode, 'is_available': availability.is_available})
        except PincodeAvailability.DoesNotExist:
            return Response({'pincode': pincode, 'is_available': False}, status=status.HTTP_404_NOT_FOUND)


class CalculateShipping(APIView):
    def get(self, request, pincode):
        try:
            rate = ShippingRate.objects.get(pincode=pincode)
            return Response(
                {'pincode': pincode, 'rate': rate.rate, 'estimated_delivery_days': rate.estimated_delivery_days})
        except ShippingRate.DoesNotExist:
            return Response({'error': 'Shipping information not available for this pincode'},
                            status=status.HTTP_404_NOT_FOUND)


class ShippingProviderViewSet(BaseViewSet):
    controller = ShippingProviderController()
    serializer = ShippingProviderSerializer
    create_schema = ShippingProviderCreateSchema
    update_schema = ShippingProviderUpdateSchema
    list_schema = ShippingProviderListSchema
    cache_key_retrieve = CacheKeys.SHIPPING_PROVIDER_DETAILS_BY_PK
    cache_key_list = CacheKeys.SHIPPING_PROVIDER_LIST

    @extend_schema(
        description="Create a new Shipping Provider",
        request=ShippingProviderCreateSchema,
        responses={201: ShippingProviderSerializer},
        examples=[
            OpenApiExample(
                name="Create Shipping Provider Example",
                description="Example payload for creating a new shipping provider.",
                value={
                    "name": "Example Shipping Provider",
                    "tracking_url_template": "http://example.com/track?code={code}",
                    "api_endpoint": "http://api.example.com",
                    "api_key": "secret_api_key",
                },
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing Shipping Provider",
        request=ShippingProviderUpdateSchema,
        responses={200: ShippingProviderSerializer},
        examples=[
            OpenApiExample(
                name="Update Shipping Provider Example",
                description="Example payload for updating an existing shipping provider.",
                value={
                    "name": "Updated Shipping Provider",
                    "tracking_url_template": "http://updated.example.com/track?code={code}",
                    "api_endpoint": "http://api.updated.example.com",
                    "api_key": "updated_secret_api_key",
                },
            ),
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List all Shipping Providers",
        responses={200: ShippingProviderSerializer(many=True)},
        parameters=[
            OpenApiParameter(name='name', type=str, description='Filter by shipping provider name'),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific Shipping Provider by ID",
        responses={200: ShippingProviderSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)


class ShipmentViewSet(BaseViewSet):
    controller = ShipmentController()
    serializer = ShipmentSerializer
    create_schema = ShipmentCreateSchema
    update_schema = ShipmentUpdateSchema
    list_schema = ShipmentListSchema
    cache_key_retrieve = CacheKeys.SHIPMENT_DETAILS_BY_PK
    cache_key_list = CacheKeys.SHIPMENT_LIST

    @extend_schema(
        description="Create a new Shipment",
        request=ShipmentCreateSchema,
        responses={201: ShipmentSerializer},
        examples=[
            OpenApiExample(
                name="Create Shipment Example",
                description="Example payload for creating a new shipment.",
                value={
                    "order_id": 1,
                    "provider_id": 2,
                    "tracking_number": "TRACK123456",
                    "shipped_date": "2024-01-01T00:00:00Z",
                    "estimated_delivery_date": "2024-01-05T00:00:00Z",
                    "actual_delivery_date": "2024-01-04T00:00:00Z",
                    "status": 1
                },
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing Shipment",
        request=ShipmentUpdateSchema,
        responses={200: ShipmentSerializer},
        examples=[
            OpenApiExample(
                name="Update Shipment Example",
                description="Example payload for updating an existing shipment.",
                value={
                    "order_id": 1,
                    "provider_id": 2,
                    "tracking_number": "TRACK123456UPDATED",
                    "shipped_date": "2024-01-02T00:00:00Z",
                    "estimated_delivery_date": "2024-01-06T00:00:00Z",
                    "actual_delivery_date": "2024-01-05T00:00:00Z",
                    "status": 1
                },
            ),
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List all Shipments",
        responses={200: ShipmentSerializer(many=True)},
        parameters=[
            OpenApiParameter(name='order_id', type=int, description='Filter by order ID'),
            OpenApiParameter(name='provider_id', type=int, description='Filter by shipping provider ID'),
            OpenApiParameter(name='status', type=str, description='Filter by shipment status'),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific Shipment by ID",
        responses={200: ShipmentSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)


class DeliveryStatusViewSet(BaseViewSet):
    controller = DeliveryStatusController()
    serializer = DeliveryStatusSerializer
    create_schema = DeliveryStatusCreateSchema
    update_schema = DeliveryStatusUpdateSchema
    list_schema = DeliveryStatusListSchema
    cache_key_retrieve = CacheKeys.DELIVERY_STATUS_DETAILS_BY_PK
    cache_key_list = CacheKeys.DELIVERY_STATUS_LIST

    @extend_schema(
        description="Create a new Delivery Status",
        request=DeliveryStatusCreateSchema,
        responses={201: DeliveryStatusSerializer},
        examples=[
            OpenApiExample(
                name="Create Delivery Status Example",
                description="Example payload for creating a new delivery status.",
                value={
                    "shipment_id": 1,
                    "status": 1,
                    "status_date": "2024-01-01T00:00:00Z",
                    "location": "Distribution Center",
                    "notes": "Package is on its way"
                },
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing Delivery Status",
        request=DeliveryStatusUpdateSchema,
        responses={200: DeliveryStatusSerializer},
        examples=[
            OpenApiExample(
                name="Update Delivery Status Example",
                description="Example payload for updating an existing delivery status.",
                value={
                    "shipment_id": 1,
                    "status": 1,
                    "status_date": "2024-01-02T00:00:00Z",
                    "location": "Local Post Office",
                    "notes": "Out for delivery"
                },
            ),
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List all Delivery Statuses",
        responses={200: DeliveryStatusSerializer(many=True)},
        parameters=[
            OpenApiParameter(name='shipment_id', type=int, description='Filter by shipment ID'),
            OpenApiParameter(name='status', type=str, description='Filter by delivery status'),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific Delivery Status by ID",
        responses={200: DeliveryStatusSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)
