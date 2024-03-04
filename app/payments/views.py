import json

import razorpay
from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.decorators import action

from app.customers.controllers import CartItemController
from app.customers.serializers import CartItemSerializer
from app.payments.controllers import PaymentController, ReturnController, RefundController, ReturnItemController
from app.payments.schemas import PaymentCreateSchema, PaymentUpdateSchema, PaymentListSchema, ReturnCreateSchema, \
    ReturnUpdateSchema, ReturnListSchema, RefundCreateSchema, RefundUpdateSchema, RefundListSchema, \
    ReturnItemCreateSchema, ReturnItemUpdateSchema, ReturnItemListSchema
from app.payments.serializers import PaymentSerializer, ReturnSerializer, RefundSerializer, ReturnItemSerializer
from app.utils.constants import CacheKeys
from app.customers.models import CartItem
from app.orders.models import Order, OrderItem
from app.utils.views import BaseViewSet


class RazorpayViewSet(BaseViewSet):
    controller = PaymentController()
    serializer = PaymentSerializer
    create_schema = PaymentCreateSchema
    update_schema = PaymentUpdateSchema
    list_schema = PaymentListSchema
    cache_key_retrieve = CacheKeys.PAYMENT_DETAILS_BY_PK
    cache_key_list = CacheKeys.PAYMENT_LIST

    @action(detail=False, methods=['post'], url_path='create-order')
    def create_order(self, request, *args, **kwargs):
        user = request.user

        cart_items = user.cart_items.all()
        total_amount = sum(item.product_variant.buying_price * item.quantity for item in cart_items)

        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user=user,
                    total_amount=total_amount)
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product_variant=cart_item.product_variant,
                        quantity=cart_item.quantity,
                        price=cart_item.price * cart_item.quantity,
                        # price=cart_item.product_variant.buying_price * cart_item.quantity
                    )

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment_data = {
                'amount': int(total_amount * 100),
                'currency': 'INR',
                'receipt': f'order_{order.id}',
                'payment_capture': '1'
            }
            orderData = client.order.create(data=payment_data)
            order.razorpay_order_id = orderData['id']
            order.save()

            return JsonResponse({'order_id': orderData['id']})

        except Exception as e:
            print(str(e))
            return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)

    @action(detail=False, methods=['post'], url_path='checkout')
    def checkout(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(user=request.user)
        total_amount = sum(item.price * item.quantity for item in cart_items)
        # total_amount = sum(item.product_variant.buying_price * item.quantity for item in cart_items)

        cart_count = cart_items.count()
        email = request.user.email
        full_name = request.user.name

        context = {
            'cart_count': cart_count,
            'cart_items': CartItemController().serialize_queryset(cart_items, serializer_override=CartItemSerializer),
            'total_amount': total_amount,
            'email': email,
            'full_name': full_name
        }
        return JsonResponse(data=context, status=200)

    @action(detail=False, methods=['post'], url_path='handle-payment')
    def handle_payment(self, request, *args, **kwargs):
        data = json.loads(request.body)
        razorpay_order_id = data.get('order_id')
        payment_id = data.get('payment_id')

        try:
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment = client.payment.fetch(payment_id)

            if payment['status'] == 'captured':
                with transaction.atomic():
                    order.payment_status = True
                    order.save()
                    user = request.user
                    user.cart_items.all().delete()
                return JsonResponse({'message': 'Payment successful'})
            else:
                return JsonResponse({'message': 'Payment failed'})

        except Order.DoesNotExist:
            return JsonResponse({'message': 'Invalid Order ID'})
        except Exception as e:

            print(str(e))
            return JsonResponse({'message': 'Server error, please try again later.'})


class PaymentViewSet(BaseViewSet):
    controller = PaymentController()
    serializer = PaymentSerializer
    create_schema = PaymentCreateSchema
    update_schema = PaymentUpdateSchema
    list_schema = PaymentListSchema
    cache_key_retrieve = CacheKeys.PAYMENT_DETAILS_BY_PK
    cache_key_list = CacheKeys.PAYMENT_LIST

    @extend_schema(
        description="Create a new Payment",
        request=PaymentCreateSchema,
        responses={201: PaymentSerializer},
        examples=[
            OpenApiExample(
                name="Create Payment Example",
                description="Example payload for creating a new payment.",
                value={
                    "order_id": 1,
                    "amount": 100.00,
                    "payment_method": 1,  # Assuming enum value representation
                    "payment_status": 1,  # Assuming enum value representation
                    "transaction_id": "txn_123456789",
                    "metadata": {"key": "value"}
                },
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing Payment",
        request=PaymentUpdateSchema,
        responses={200: PaymentSerializer},
        examples=[
            OpenApiExample(
                name="Update Payment Example",
                description="Example payload for updating an existing payment.",
                value={
                    "order_id": 1,
                    "amount": 150.00,
                    "payment_method": 2,  # Assuming enum value representation
                    "payment_status": 2,  # Assuming enum value representation
                    "transaction_id": "txn_987654321",
                    "metadata": {"updated_key": "updated_value"}
                },
            ),
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List all Payments",
        responses={200: PaymentSerializer(many=True)},
        parameters=[
            OpenApiParameter(name='order_id', type=int, description='Filter by order ID'),
            OpenApiParameter(name='payment_method', type=int, description='Filter by payment method'),
            OpenApiParameter(name='payment_status', type=int, description='Filter by payment status'),
            OpenApiParameter(name='transaction_id', type=str, description='Filter by transaction ID'),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific Payment by ID",
        responses={200: PaymentSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)


class ReturnViewSet(BaseViewSet):
    controller = ReturnController()
    serializer = ReturnSerializer
    create_schema = ReturnCreateSchema
    update_schema = ReturnUpdateSchema
    list_schema = ReturnListSchema
    cache_key_retrieve = CacheKeys.RETURN_DETAILS_BY_PK
    cache_key_list = CacheKeys.RETURN_LIST

    @extend_schema(
        description="Create a new Return",
        request=ReturnCreateSchema,
        responses={201: ReturnSerializer},
        examples=[
            OpenApiExample(
                name="Create Return Example",
                description="Example payload for creating a new return.",
                value={
                    "order_id": 1,
                    "reason": "Received damaged product",
                    "status": 1,  # Assuming enum value representation for REQUESTED
                },
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing Return",
        request=ReturnUpdateSchema,
        responses={200: ReturnSerializer},
        examples=[
            OpenApiExample(
                name="Update Return Example",
                description="Example payload for updating an existing return.",
                value={
                    "order_id": 1,
                    "reason": "Product was not as expected",
                    "status": 2,  # Assuming enum value representation for different status
                },
            ),
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List all Returns",
        responses={200: ReturnSerializer(many=True)},
        parameters=[
            OpenApiParameter(name='order_id', type=int, description='Filter by order ID'),
            OpenApiParameter(name='status', type=int, description='Filter by return status'),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific Return by ID",
        responses={200: ReturnSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)


class RefundViewSet(BaseViewSet):
    controller = RefundController()
    serializer = RefundSerializer
    create_schema = RefundCreateSchema
    update_schema = RefundUpdateSchema
    list_schema = RefundListSchema
    cache_key_retrieve = CacheKeys.REFUND_DETAILS_BY_PK
    cache_key_list = CacheKeys.REFUND_LIST

    @extend_schema(
        description="Create a new Refund",
        request=RefundCreateSchema,
        responses={201: RefundSerializer},
        examples=[
            OpenApiExample(
                name="Create Refund Example",
                description="Example payload for creating a new refund.",
                value={
                    "return_id": 1,
                    "payment_id": 1,
                    "refund_type": 1,  # Assuming enum value representation
                    "amount": 100.00,
                    "reason": "Product returned, refund initiated",
                    "status": 1,  # Assuming enum for INITIATED
                    "metadata": {"extra_info": "Handled manually"},
                },
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing Refund",
        request=RefundUpdateSchema,
        responses={200: RefundSerializer},
        examples=[
            OpenApiExample(
                name="Update Refund Example",
                description="Example payload for updating an existing refund.",
                value={
                    "return_id": 1,
                    "payment_id": 1,
                    "refund_type": 2,  # Assuming enum value representation for a different type
                    "amount": 150.00,
                    "reason": "Product return processing fee deducted",
                    "status": 2,  # Assuming enum for a different status
                    "metadata": {"extra_info": "Adjusted amount"},
                },
            ),
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List all Refunds",
        responses={200: RefundSerializer(many=True)},
        parameters=[
            OpenApiParameter(name='return_id', type=int, description='Filter by return ID'),
            OpenApiParameter(name='payment_id', type=int, description='Filter by payment ID'),
            OpenApiParameter(name='refund_type', type=int, description='Filter by refund type'),
            OpenApiParameter(name='status', type=int, description='Filter by refund status'),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific Refund by ID",
        responses={200: RefundSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)


class ReturnItemViewSet(BaseViewSet):
    controller = ReturnItemController()
    serializer = ReturnItemSerializer
    create_schema = ReturnItemCreateSchema
    update_schema = ReturnItemUpdateSchema
    list_schema = ReturnItemListSchema
    cache_key_retrieve = CacheKeys.RETURN_ITEM_DETAILS_BY_PK
    cache_key_list = CacheKeys.RETURN_ITEM_LIST

    @extend_schema(
        description="Create a new Return Item",
        request=ReturnItemCreateSchema,
        responses={201: ReturnItemSerializer},
        examples=[
            OpenApiExample(
                name="Create Return Item Example",
                description="Example payload for creating a new return item.",
                value={
                    "return_id": 1,
                    "product_variant_id": 1,
                    "quantity": 2,
                },
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing Return Item",
        request=ReturnItemUpdateSchema,
        responses={200: ReturnItemSerializer},
        examples=[
            OpenApiExample(
                name="Update Return Item Example",
                description="Example payload for updating an existing return item.",
                value={
                    "return_id": 1,
                    "product_variant_id": 1,
                    "quantity": 1,  # Updating the quantity
                },
            ),
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List all Return Items",
        responses={200: ReturnItemSerializer(many=True)},
        parameters=[
            OpenApiParameter(name='return_id', type=int, description='Filter by return ID'),
            OpenApiParameter(name='product_variant_id', type=int, description='Filter by product variant ID'),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific Return Item by ID",
        responses={200: ReturnItemSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)
