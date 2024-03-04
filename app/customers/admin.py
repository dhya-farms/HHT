from django.contrib import admin
from app.customers.models import Customer, Address, Wishlist, WishlistItem, Review, CartItem
from django.utils.html import format_html
from django.urls import reverse


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1


class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 1


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'view_addresses_link')
    search_fields = ('user__username', 'user__email')
    inlines = [AddressInline, ReviewInline]

    def get_username(self, obj):
        return obj.user.username

    get_username.admin_order_field = 'user__username'
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email

    get_email.admin_order_field = 'user__email'
    get_email.short_description = 'Email'

    def view_addresses_link(self, obj):
        url = (
            reverse("admin:app_address_changelist")
            + "?"
            + "customer__id__exact={}".format(obj.pk)
        )
        return format_html('<a href="{}">View Addresses</a>', url)

    view_addresses_link.short_description = "Addresses"


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'address_type', 'street', 'city', 'state', 'zip_code', 'country', 'is_primary')
    list_filter = ('address_type', 'city', 'state', 'country', 'is_primary')
    search_fields = ('street', 'city', 'zip_code')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('customer', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)
    inlines = [WishlistItemInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('product__name',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_variant', 'quantity', 'price', 'added_at')
    search_fields = ('product_variant__name',)
