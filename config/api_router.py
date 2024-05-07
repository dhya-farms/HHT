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

router.register("users", UserViewSet, basename="users")
router.register("otp", OtpLoginViewSet, basename='otp')
router.register("customers", CustomerViewSet, basename="customers")
router.register("addresses", AddressViewSet, basename="addresses")
router.register("wishlists", WishlistViewSet, basename="wishlists")
router.register("wishlist-items", WishlistItemViewSet, basename="wishlist-items")
router.register("reviews", ReviewViewSet, basename="reviews")
router.register("cart-items", CartItemViewSet, basename="cart-items")
router.register("orders", OrderViewSet, basename="orders")
router.register("order-items", OrderItemViewSet, basename="order-items")
router.register("payments", RazorpayViewSet, basename="payments")
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
router.register("products", ProductViewSet, basename="products")
router.register("product-variants", ProductVariantViewSet, basename="product-variants")
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


