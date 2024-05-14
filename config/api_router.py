from django.conf import settings
from django.urls import path
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView, SpectacularRedocView
from rest_framework.routers import DefaultRouter, SimpleRouter

from app.customers.views import CustomerViewSet, AddressViewSet, WishlistViewSet, WishlistItemViewSet, ReviewViewSet, \
    CartItemViewSet
from app.orders.views import OrderViewSet, OrderItemViewSet
from app.payments.views import PaymentViewSet, RefundViewSet, ReturnItemViewSet, ReturnViewSet, RazorpayViewSet
from app.products.views import CategoryViewSet, SupplierViewSet, TagViewSet, CouponViewSet, ProductViewSet, \
    ProductVariantViewSet, ProductImageViewSet, AttributeViewSet, AttributeValueViewSet, CollectionViewSet
from app.shippings.views import ShippingProviderViewSet, DeliveryStatusViewSet, ShipmentViewSet, \
    CheckPincodeAvailability, CalculateShipping
from app.users.views import UserViewSet, OtpLoginViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# users login with phone numbers to get their tokens so that they can access all the APIs, still users can see
# products without tokens, but they can only see.
router.register("otp", OtpLoginViewSet, basename='otp')

# After Login, we heve user model instance only with their mobile numbers and tokens, we need to update profile
router.register("users", UserViewSet, basename="users")

# while checkout or on profile page there will be  address page, user can add one or more address with address types one home one office many others
router.register("addresses", AddressViewSet, basename="addresses")

# list all the products and (add_to_favouries, remove_from_favouries, my-favourites) -> based on user
router.register("products", ProductViewSet, basename="products")


# list all variants based on product, (add_to_cart, remove_from_cart, increase_cart_item, decrease_cart_item) -> based on user
router.register("product-variants", ProductVariantViewSet, basename="product-variants")

# list cart items based on user id
router.register("cart-items", CartItemViewSet, basename="cart-items")


# create_order - will get address_id for shipping and billing for Order and create orders and order items and
# also create order on razorpay table and will return
# JsonResponse({
#           'callback_url': f'{full_url}/hht/api/payments/handle-payment/',   - our own api
#           "razorpay_key": settings.RAZOR_KEY_ID,
#           "order_id": orderData['id']  - razorpay order's id
#},
# checkout - just show cart items added by user
# handle_payment - refer https://medium.com/scalereal/razorpay-payment-gateway-integration-with-django-c422ba38f978
# and Razor pay documentation for web integrations
# once we process the payments and it successfull cart items got deleted from table and
# we generate an invoice and store to AWS S3, please refer below orders
router.register("payments", RazorpayViewSet, basename="payments")

# invoice_link api
router.register("orders", OrderViewSet, basename="orders")


router.register("customers", CustomerViewSet, basename="customers")
router.register("wishlists", WishlistViewSet, basename="wishlists")
router.register("wishlist-items", WishlistItemViewSet, basename="wishlist-items")
router.register("reviews", ReviewViewSet, basename="reviews")
router.register("order-items", OrderItemViewSet, basename="order-items")
# router.register("payments", PaymentViewSet, basename="payments")
router.register("returns", ReturnViewSet, basename="returns")
router.register("refunds", RefundViewSet, basename="refunds")
router.register("return-items", ReturnItemViewSet, basename="return-items")
router.register("shipping-providers", ShippingProviderViewSet, basename="shipping-providers")
router.register("shipments", ShipmentViewSet, basename="shipments")
router.register("delivery-statuses", DeliveryStatusViewSet, basename="delivery-statuses")
router.register("categories", CategoryViewSet, basename="categories")
router.register("collections", CollectionViewSet, basename="collections")
router.register("suppliers", SupplierViewSet, basename="suppliers")
router.register("tags", TagViewSet, basename="tags")
router.register("coupons", CouponViewSet, basename="coupons")
router.register("product-images", ProductImageViewSet, basename="product-images")
router.register("attributes", AttributeViewSet, basename="attributes")
router.register("attribute-values", AttributeValueViewSet, basename="attribute-values")

app_name = "api"
urlpatterns = router.urls

urlpatterns += [
    path('shipping/check-pincode/<str:pincode>/', CheckPincodeAvailability.as_view(), name='check-pincode'),
    path('shipping/calculate-shipping/<str:pincode>/', CalculateShipping.as_view(), name='calculate-shipping'),
    path('products/<slug:slug>/', ProductViewSet.as_view({'get': 'retrieve'}), name='product-detail'),
    # path('get-enum-values/', get_enum_values, name='get_enum_values'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='api:schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='api:schema'), name='redoc'),
]


