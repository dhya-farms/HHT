import boto3
from botocore.exceptions import NoCredentialsError
from django.http import HttpResponseRedirect, HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from rest_framework.decorators import action

from config import settings
from .models import Order
from app.orders.controllers import OrderController, OrderItemController
from app.orders.serializers import OrderSerializer, OrderItemSerializer
from app.orders.schemas import OrderCreateSchema, OrderUpdateSchema, OrderListSchema, OrderItemCreateSchema, \
    OrderItemUpdateSchema, OrderItemListSchema
from app.utils.constants import CacheKeys
from app.utils.views import BaseViewSet


class OrderViewSet(BaseViewSet):
    controller = OrderController()
    serializer = OrderSerializer
    create_schema = OrderCreateSchema
    update_schema = OrderUpdateSchema
    list_schema = OrderListSchema
    cache_key_retrieve = CacheKeys.ORDER_DETAILS_BY_PK
    cache_key_list = CacheKeys.ORDER_LIST

    @extend_schema(
        description="Create a new Order",
        request=OrderCreateSchema,
        responses={201: OrderSerializer},
        examples=[
            OpenApiExample(
                name="Create Order Example",
                description="Example payload for creating a new order.",
                value={
                    "customer_id": 1,
                    "coupon_id": 2,
                    "status": 1
                },
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing Order",
        request=OrderUpdateSchema,
        responses={200: OrderSerializer},
        examples=[
            OpenApiExample(
                name="Update Order Example",
                description="Example payload for updating an existing order.",
                value={
                    "customer_id": 1,
                    "coupon_id": 3,
                    "status": 1
                },
            ),
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List all Orders",
        responses={200: OrderSerializer(many=True)},
        parameters=[
            OpenApiParameter(name='customer_id', type=int, description='Filter by customer ID'),
            OpenApiParameter(name='coupon_id', type=int, description='Filter by coupon ID'),
            OpenApiParameter(name='status', type=str, description='Filter by order status')
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific Order by ID",
        responses={200: OrderSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)

    @extend_schema(
        description="Retrieve a Invoice by Order ID",
    )
    @action(detail=True, methods=['get'], url_path='invoice')
    def invoice(self, request, pk, *args, **kwargs):
        order = Order.objects.get(pk=pk, user=request.user)

        # Assume invoice_file is a FileField storing the file in S3
        invoice_file_path = order.invoice_file.name

        s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                 region_name=settings.AWS_S3_REGION_NAME)

        try:
            signed_url = s3_client.generate_presigned_url('get_object',
                                                          Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                                  'Key': invoice_file_path},
                                                          ExpiresIn=3600)
            return HttpResponseRedirect(signed_url)
        except NoCredentialsError:
            return HttpResponse("Error generating Invoice URL", status=500)


class OrderItemViewSet(BaseViewSet):
    controller = OrderItemController()
    serializer = OrderItemSerializer
    create_schema = OrderItemCreateSchema
    update_schema = OrderItemUpdateSchema
    list_schema = OrderItemListSchema
    cache_key_retrieve = CacheKeys.ORDER_ITEM_DETAILS_BY_PK
    cache_key_list = CacheKeys.ORDER_ITEM_LIST

    @extend_schema(
        description="Create a new OrderItem",
        request=OrderItemCreateSchema,
        responses={201: OrderItemSerializer},
        examples=[
            OpenApiExample(
                name="Create OrderItem Example",
                description="Example payload for creating a new order item.",
                value={
                    "order_id": 1,
                    "product_variant_id": 1,
                    "quantity": 2,
                    "price": 100.00
                },
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing OrderItem",
        request=OrderItemUpdateSchema,
        responses={200: OrderItemSerializer},
        examples=[
            OpenApiExample(
                name="Update OrderItem Example",
                description="Example payload for updating an existing order item.",
                value={
                    "order_id": 1,
                    "product_variant_id": 1,
                    "quantity": 3,
                    "price": 150.00
                },
            ),
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List all OrderItems",
        responses={200: OrderItemSerializer(many=True)},
        parameters=[
            OpenApiParameter(name='order_id', type=int, description='Filter by order ID'),
            OpenApiParameter(name='product_variant_id', type=int, description='Filter by product variant ID')
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific OrderItem by ID",
        responses={200: OrderItemSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)
