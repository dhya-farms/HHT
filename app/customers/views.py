from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample

from .models import Customer
from app.customers.controllers import CustomerController, AddressController, WishlistController, WishlistItemController, \
    ReviewController, CartItemController
from app.customers.serializers import CustomerSerializer, AddressSerializer, WishlistSerializer, WishlistItemSerializer, \
    ReviewSerializer, CartItemSerializer
from app.customers.schemas import CustomerCreateSchema, CustomerUpdateSchema, CustomerListSchema, AddressCreateSchema, \
    AddressUpdateSchema, AddressListSchema, WishlistCreateSchema, WishlistUpdateSchema, WishlistListSchema, \
    WishlistItemCreateSchema, WishlistItemUpdateSchema, WishlistItemListSchema, ReviewCreateSchema, ReviewUpdateSchema, \
    ReviewListSchema, CartItemCreateSchema, CartItemUpdateSchema, CartItemListSchema
from ..utils.constants import CacheKeys
from ..utils.views import BaseViewSet


class CustomerViewSet(BaseViewSet):
    controller = CustomerController()
    serializer = CustomerSerializer
    create_schema = CustomerCreateSchema
    update_schema = CustomerUpdateSchema
    list_schema = CustomerListSchema
    cache_key_retrieve = CacheKeys.CUSTOMER_DETAILS_BY_PK  # Update as needed
    cache_key_list = CacheKeys.CUSTOMER_LIST  # Update as needed

    @extend_schema(
        description="Create a new Customer",
        request=CustomerCreateSchema,
        responses={201: CustomerSerializer},
        examples=[
            OpenApiExample(
                name="Create Customer Example",
                description="Example payload for creating a new customer.",
                value={
                    "user_id": 1,
                },
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing Customer",
        request=CustomerUpdateSchema,
        responses={200: CustomerSerializer},
        examples=[
            OpenApiExample(
                name="Update Customer Example",
                description="Example payload for updating an existing customer.",
                value={
                    "user_id": 2,
                },
            ),
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List all Customers",
        responses={200: CustomerSerializer(many=True)},
        parameters=[
            OpenApiParameter(name='user_id', type=int, description='Filter by user ID'),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific Customer by ID",
        responses={200: CustomerSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)

    @extend_schema(
        description="Make a Customer inactive (Custom Action Example)",
        methods=['POST'],
        responses={200: OpenApiResponse(description="Customer inactivated successfully")}
    )
    @action(detail=True, methods=['post'], url_path='make-inactive')
    def make_inactive(self, request, pk, *args, **kwargs):
        # Custom action to make a customer inactive
        # Implement the actual logic here
        return Response({"message": "Customer marked as inactive"})


class AddressViewSet(BaseViewSet):
    controller = AddressController()
    serializer = AddressSerializer
    create_schema = AddressCreateSchema
    update_schema = AddressUpdateSchema
    list_schema = AddressListSchema
    cache_key_retrieve = CacheKeys.ADDRESS_DETAILS_BY_PK
    cache_key_list = CacheKeys.ADDRESS_LIST

    @extend_schema(
        description="Create a new Address",
        request=AddressCreateSchema,
        responses={201: AddressSerializer},
        examples=[
            OpenApiExample(
                name="Create Address Example",
                description="Example payload for creating a new address.",
                value={
                    "customer_id": 1,
                    "address_type": "HOME",
                    "street": "123 Main St",
                    "city": "Cityville",
                    "state": "State",
                    "zip_code": "12345",
                    "country": "Country",
                    "is_primary": True
                },
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing Address",
        request=AddressUpdateSchema,
        responses={200: AddressSerializer},
        examples=[
            OpenApiExample(
                name="Update Address Example",
                description="Example payload for updating an existing address.",
                value={
                    "customer_id": 1,
                    "address_type": "OFFICE",
                    "street": "456 Secondary St",
                    "city": "Metropolis",
                    "state": "State",
                    "zip_code": "67890",
                    "country": "Country",
                    "is_primary": False
                },
            ),
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List all Addresses",
        responses={200: AddressSerializer(many=True)},
        parameters=[
            OpenApiParameter(name='customer_id', type=int, description='Filter by customer ID'),
            OpenApiParameter(name='city', type=str, description='Filter by city name'),
            OpenApiParameter(name='is_primary', type=bool, description='Filter by primary status')
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific Address by ID",
        responses={200: AddressSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)


class WishlistViewSet(BaseViewSet):
    controller = WishlistController()
    serializer = WishlistSerializer
    create_schema = WishlistCreateSchema
    update_schema = WishlistUpdateSchema
    list_schema = WishlistListSchema
    cache_key_retrieve = CacheKeys.WISHLIST_DETAILS_BY_PK
    cache_key_list = CacheKeys.WISHLIST_LIST

    @extend_schema(
        description="Create a new Wishlist",
        request=WishlistCreateSchema,
        responses={201: WishlistSerializer},
        examples=[
            OpenApiExample(
                name="Create Wishlist Example",
                description="Example payload for creating a new wishlist.",
                value={
                    "customer_id": 1,
                    "name": "My Wishlist"
                },
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing Wishlist",
        request=WishlistUpdateSchema,
        responses={200: WishlistSerializer},
        examples=[
            OpenApiExample(
                name="Update Wishlist Example",
                description="Example payload for updating an existing wishlist.",
                value={
                    "customer_id": 1,
                    "name": "Updated Wishlist Name"
                },
            ),
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List all Wishlists",
        responses={200: WishlistSerializer(many=True)},
        parameters=[
            OpenApiParameter(name='customer_id', type=int, description='Filter by customer ID'),
            OpenApiParameter(name='name', type=str, description='Filter by wishlist name')
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific Wishlist by ID",
        responses={200: WishlistSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)


class WishlistItemViewSet(BaseViewSet):
    controller = WishlistItemController()
    serializer = WishlistItemSerializer
    create_schema = WishlistItemCreateSchema
    update_schema = WishlistItemUpdateSchema
    list_schema = WishlistItemListSchema
    cache_key_retrieve = CacheKeys.WISHLIST_ITEM_DETAILS_BY_PK
    cache_key_list = CacheKeys.WISHLIST_ITEM_LIST

    @extend_schema(
        description="Create a new WishlistItem",
        request=WishlistItemCreateSchema,
        responses={201: WishlistItemSerializer},
        examples=[
            OpenApiExample(
                name="Create WishlistItem Example",
                description="Example payload for creating a new wishlist item.",
                value={
                    "wishlist_id": 1,
                    "product_variant_id": 2
                },
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing WishlistItem",
        request=WishlistItemUpdateSchema,
        responses={200: WishlistItemSerializer},
        examples=[
            OpenApiExample(
                name="Update WishlistItem Example",
                description="Example payload for updating an existing wishlist item.",
                value={
                    "wishlist_id": 1,
                    "product_variant_id": 3
                },
            ),
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List all WishlistItems",
        responses={200: WishlistItemSerializer(many=True)},
        parameters=[
            OpenApiParameter(name='wishlist_id', type=int, description='Filter by wishlist ID'),
            OpenApiParameter(name='product_variant_id', type=int, description='Filter by product variant ID')
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific WishlistItem by ID",
        responses={200: WishlistItemSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)


class ReviewViewSet(BaseViewSet):
    controller = ReviewController()
    serializer = ReviewSerializer
    create_schema = ReviewCreateSchema
    update_schema = ReviewUpdateSchema
    list_schema = ReviewListSchema
    cache_key_retrieve = CacheKeys.REVIEW_DETAILS_BY_PK
    cache_key_list = CacheKeys.REVIEW_LIST

    @extend_schema(
        description="Create a new Review",
        request=ReviewCreateSchema,
        responses={201: ReviewSerializer},
        examples=[
            OpenApiExample(
                name="Create Review Example",
                description="Example payload for creating a new review.",
                value={
                    "customer_id": 1,
                    "product_id": 2,
                    "rating": 5,
                    "comment": "Great product!"
                },
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing Review",
        request=ReviewUpdateSchema,
        responses={200: ReviewSerializer},
        examples=[
            OpenApiExample(
                name="Update Review Example",
                description="Example payload for updating an existing review.",
                value={
                    "customer_id": 1,
                    "product_id": 2,
                    "rating": 4,
                    "comment": "Good product, but could be better."
                },
            ),
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List all Reviews",
        responses={200: ReviewSerializer(many=True)},
        parameters=[
            OpenApiParameter(name='customer_id', type=int, description='Filter by customer ID'),
            OpenApiParameter(name='product_id', type=int, description='Filter by product ID'),
            OpenApiParameter(name='rating', type=int, description='Filter by rating')
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific Review by ID",
        responses={200: ReviewSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)


class CartItemViewSet(BaseViewSet):
    controller = CartItemController()
    serializer = CartItemSerializer
    create_schema = CartItemCreateSchema
    update_schema = CartItemUpdateSchema
    list_schema = CartItemListSchema
    cache_key_retrieve = CacheKeys.CART_ITEM_DETAILS_BY_PK
    cache_key_list = CacheKeys.CART_ITEM_LIST

    @extend_schema(
        description="Create a new CartItem",
        request=CartItemCreateSchema,
        responses={201: CartItemSerializer},
        examples=[
            OpenApiExample(
                name="Create CartItem Example",
                description="Example payload for creating a new cart item.",
                value={
                    "customer_id": 1,
                    "product_variant_id": 2,
                    "quantity": 1,
                    "price": 100.00
                },
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing CartItem",
        request=CartItemUpdateSchema,
        responses={200: CartItemSerializer},
        examples=[
            OpenApiExample(
                name="Update CartItem Example",
                description="Example payload for updating an existing cart item.",
                value={
                    "customer_id": 1,
                    "product_variant_id": 2,
                    "quantity": 2,
                    "price": 95.00
                },
            ),
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List all CartItems",
        responses={200: CartItemSerializer(many=True)},
        parameters=[
            OpenApiParameter(name='customer_id', type=int, description='Filter by customer ID'),
            OpenApiParameter(name='product_variant_id', type=int, description='Filter by product variant ID')
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific CartItem by ID",
        responses={200: CartItemSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)
