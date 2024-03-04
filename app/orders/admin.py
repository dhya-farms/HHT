from django.contrib import admin
from app.orders.models import Order, OrderItem
from django.utils.html import format_html
from django.urls import reverse


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ('product_variant', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_coupon_code', 'status', 'created_at', 'view_order_items_link')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('id', 'user__username', 'coupon__code')
    inlines = [OrderItemInline]

    def get_coupon_code(self, obj):
        return obj.coupon.code if obj.coupon else '-'

    get_coupon_code.short_description = 'Coupon Code'

    def view_order_items_link(self, obj):
        url = (
            reverse("admin:app_orderitem_changelist")
            + "?"
            + "order__id__exact={}".format(obj.pk)
        )
        return format_html('<a href="{}">View Order Items</a>', url)

    view_order_items_link.short_description = "Order Items"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_variant', 'quantity', 'price')
    list_filter = ('order__status', 'product_variant')
    search_fields = ('order__id', 'product_variant__name')
