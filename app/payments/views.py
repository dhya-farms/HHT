import json

import razorpay
from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status, viewsets
from rest_framework.decorators import action

from app.customers.controllers import CartItemController
from app.customers.serializers import CartItemSerializer, AddressSerializer
from app.payments.controllers import PaymentController, ReturnController, RefundController, ReturnItemController
from app.payments.schemas import PaymentCreateSchema, PaymentUpdateSchema, PaymentListSchema, ReturnCreateSchema, \
    ReturnUpdateSchema, ReturnListSchema, RefundCreateSchema, RefundUpdateSchema, RefundListSchema, \
    ReturnItemCreateSchema, ReturnItemUpdateSchema, ReturnItemListSchema
from app.payments.serializers import PaymentSerializer, ReturnSerializer, RefundSerializer, ReturnItemSerializer
from app.utils.constants import CacheKeys
from app.customers.models import CartItem, Address
from app.orders.models import Order, OrderItem
from app.utils.views import BaseViewSet
from app.payments.tasks import generate_and_store_invoice_pdf


class RazorpayViewSet(viewsets.ViewSet):
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

    @action(detail=False, methods=['post'], url_path='create-order')
    def create_order(self, request, *args, **kwargs):
        user = request.user
        shipping_address_id = request.data.get('shipping_address_id', None)
        billing_address_id = request.data.get('billing_address_id', None)
        cart_items = user.cart_items.all()
        total_amount = sum(item.product_variant.buying_price * item.quantity for item in cart_items)
        shipping_address = Address.objects.get(shipping_address_id)


        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user=user,
                    total_amount=total_amount,
                    shipping_address=shipping_address_id,
                    billing_address=billing_address_id
                )
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product_variant=cart_item.product_variant,
                        quantity=cart_item.quantity,
                        price=cart_item.product_variant.buying_price * cart_item.quantity
                    )
            payment_data = {
                'amount': int(total_amount * 100),
                'currency': 'INR',
                'receipt': f'order_{order.id}',
                'payment_capture': '1'
            }
            orderData = self.client.order.create(data=payment_data)
            order.razorpay_order_id = orderData['id']
            order.save()

            domain = request.get_host()
            scheme = request.scheme
            full_url = f'{scheme}://{domain}'

            return JsonResponse({
                'callback_url': f'{full_url}/hht/api/payments/handle-payment/',
                "razorpay_key": settings.RAZOR_KEY_ID,
                "order_id": orderData['id']
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(str(e))
            return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)

    @action(detail=False, methods=['post'], url_path='checkout')
    def checkout(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(user=request.user)
        # total_amount = sum(item.price * item.quantity for item in cart_items)
        total_amount = sum(item.product_variant.buying_price * item.quantity for item in cart_items)

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
        if "razorpay_signature" not in data:
            return JsonResponse({'message': 'Invalid payment data'}, status=status.HTTP_400_BAD_REQUEST)

        if not self.verify_signature(data):
            return JsonResponse({'message': 'Payment signature verification failed'},
                                status=status.HTTP_400_BAD_REQUEST)

        # Continue with processing payment since signature verification was successful
        return self.process_payment(data, request.user)

    def verify_signature(self, data):
        if settings.DEBUG:
            return True
        try:
            status = self.client.utility.verify_payment_signature(data)
            return True
        except Exception:
            return False

    def process_payment(self, data, user):
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature_id = data.get("razorpay_signature")  # Extracting the signature ID

        try:
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            if not settings.DEBUG:
                payment = self.client.payment.fetch(razorpay_payment_id)

                if payment['status'] == 'captured' and self.update_order_and_generate_invoice(razorpay_order_id,
                                                                                              razorpay_signature_id,
                                                                                              razorpay_payment_id,
                                                                                              user):
                    # self.update_order_on_success(order, razorpay_payment_id, razorpay_signature_id, user)
                    return JsonResponse({'message': 'Payment successful'}, status=status.HTTP_200_OK)
                else:
                    self.update_order_on_failure(order, razorpay_payment_id)
                    return JsonResponse({'message': 'Payment failed'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if self.update_order_and_generate_invoice(razorpay_order_id,
                                                          razorpay_signature_id,
                                                          razorpay_payment_id,
                                                          user):
                    # self.update_order_on_success(order, razorpay_payment_id, razorpay_signature_id, user)
                    return JsonResponse({'message': 'Payment successful'}, status=status.HTTP_200_OK)
                else:
                    self.update_order_on_failure(order, razorpay_payment_id)
                    return JsonResponse({'message': 'Payment failed'}, status=status.HTTP_400_BAD_REQUEST)

        except Order.DoesNotExist:
            return JsonResponse({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'message': 'Server error, please try again later'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_order_and_generate_invoice(self, razorpay_order_id, razorpay_signature_id, razorpay_payment_id, user):
        with transaction.atomic():
            order = Order.objects.select_related('user', 'shipping_address', 'billing_address') \
                .prefetch_related('items__product_variant') \
                .get(razorpay_order_id=razorpay_order_id)

            order.payment_status = True
            order.razorpay_payment_id = razorpay_payment_id
            order.razorpay_signature_id = razorpay_signature_id
            order.save()

            # Preparing line items for the invoice
            line_items = []
            for item in order.items.all():
                line_item = {
                    "name": item.product_variant.name,
                    "description": item.product_variant.short_description,
                    "amount": int(item.price * 100),  # Convert to paise
                    "currency": "INR",
                    "quantity": item.quantity,
                }
                line_items.append(line_item)

            # Invoice data for RazorPay API
            invoice_data = {
                "type": "invoice",
                "description": "",
                "date": int(order.created_at.timestamp()),
                "customer": {
                    "name": user.name,
                    "email": user.email,
                    "contact": user.mobile_no,
                    "billing_address": AddressSerializer(order.billing_address).data,
                    "shipping_address": AddressSerializer(order.shipping_address).data
                },
                "line_items": line_items,
                "currency": "INR",
                "receipt": f"Order_{order.id}",
                "notes": str(order.id)
            }

            # Generate invoice using RazorPay API
            try:
                invoice = {
                    "id": "inv_DAweOiQ7amIUVd",
                    "entity": "invoice",
                    "receipt": "#0961",
                    "invoice_number": "#0961",
                    "customer_id": "cust_DAtUWmvpktokrT",
                    "customer_details": {
                        "id": "cust_DAtUWmvpktokrT",
                        "name": "Gaurav Kumar",
                        "email": "gaurav.kumar@example.com",
                        "contact": "9977886633",
                        "gstin": None,
                        "billing_address": {
                            "id": "addr_DAtUWoxgu91obl",
                            "type": "billing_address",
                            "primary": True,
                            "line1": "318 C-Wing, Suyog Co. Housing Society Ltd.",
                            "line2": "T.P.S Road, Vazira, Borivali",
                            "pincode": "400092",
                            "city": "Mumbai",
                            "state": "Maharashtra",
                            "country": "in"
                        },
                        "shipping_address": None,
                        "customer_name": "Gaurav Kumar",
                        "customer_email": "gaurav.kumar@example.com",
                        "customer_contact": "9977886633"
                    },
                    "order_id": "order_DBG3P8ZgDd1dsG",
                    "line_items": [
                        {
                            "id": "li_DAweOizsysoJU6",
                            "item_id": None,
                            "name": "Book / English August - Updated name and quantity",
                            "description": "150 points in Quidditch",
                            "amount": 400,
                            "unit_amount": 400,
                            "gross_amount": 400,
                            "tax_amount": 0,
                            "taxable_amount": 400,
                            "net_amount": 400,
                            "currency": "INR",
                            "type": "invoice",
                            "tax_inclusive": False,
                            "hsn_code": None,
                            "sac_code": None,
                            "tax_rate": None,
                            "unit": None,
                            "quantity": 1,
                            "taxes": []
                        },
                        {
                            "id": "li_DAwjWQUo07lnjF",
                            "item_id": None,
                            "name": "Book / A Wild Sheep Chase",
                            "description": None,
                            "amount": 200,
                            "unit_amount": 200,
                            "gross_amount": 200,
                            "tax_amount": 0,
                            "taxable_amount": 200,
                            "net_amount": 200,
                            "currency": "INR",
                            "type": "invoice",
                            "tax_inclusive": False,
                            "hsn_code": None,
                            "sac_code": None,
                            "tax_rate": None,
                            "unit": None,
                            "quantity": 1,
                            "taxes": []
                        }
                    ],
                    "payment_id": None,
                    "status": "issued",
                    "expire_by": 1567103399,
                    "issued_at": 1566974805,
                    "paid_at": None,
                    "cancelled_at": None,
                    "expired_at": None,
                    "sms_status": None,
                    "email_status": None,
                    "date": 1566891149,
                    "terms": None,
                    "partial_payment": False,
                    "gross_amount": 600,
                    "tax_amount": 0,
                    "taxable_amount": 600,
                    "amount": 600,
                    "amount_paid": 0,
                    "amount_due": 600,
                    "currency": "INR",
                    "currency_symbol": "₹",
                    "description": "This is a test invoice.",
                    "notes": {
                        "updated-key": "An updated note."
                    },
                    "comment": None,
                    "short_url": "https://rzp.io/i/K8Zg72C",
                    "view_less": True,
                    "billing_start": None,
                    "billing_end": None,
                    "type": "invoice",
                    "group_taxes_discounts": False,
                    "created_at": 1566906474,
                    "idempotency_key": None
                }
                if settings.DEPLOYMENT_ENVIRONMENT == 'prod':
                    invoice = self.client.invoice.create(data=invoice_data)
                order.razorpay_invoice_id = invoice['id']
                order.save()

                # Trigger asynchronous task to generate and store invoice PDF
                generate_and_store_invoice_pdf(order, invoice)

                # Clearing the user's cart items after successful payment and invoice generation
                order.user.cart_items.all().delete()

                return order
            except Exception as e:
                # Log the exception and handle the error appropriately
                print(f"Failed to create invoice for order {order.id}: {str(e)}")
                # You might want to return an error or handle this case depending on your application's needs
                return None

    def update_order_on_failure(self, order, razorpay_payment_id):
        order.payment_status = False
        order.razorpay_payment_id = razorpay_payment_id
        order.save()


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
