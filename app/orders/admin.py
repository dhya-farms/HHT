from django.contrib import admin
from django.utils.html import format_html

from .enums import OrderStatus
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # Prevents extra empty forms
    fields = ('product_variant', 'quantity', 'price')
    readonly_fields = ('product_variant', 'quantity', 'price')

    def has_add_permission(self, request, obj=None):
        # Prevent adding more items to the order through the admin
        return False

    def has_delete_permission(self, request, obj=None):
        # Prevent deleting items from the order through the admin
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'user', 'status_display', 'payment_status_display', 'total_amount', 'created_at', 'invoice_link')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('user__username', 'user__email', 'razorpay_order_id')
    readonly_fields = ('user', 'total_amount', 'created_at', 'updated_at', 'razorpay_order_id', 'razorpay_payment_id',
                       'razorpay_signature_id', 'razorpay_invoice_id', 'invoice_file')
    inlines = [OrderItemInline]

    def status_display(self, obj):
        return OrderStatus(obj.status).label

    status_display.short_description = 'Status'

    def payment_status_display(self, obj):
        return "Paid" if obj.payment_status else "Not Paid"

    payment_status_display.short_description = 'Payment Status'

    def invoice_link(self, obj):
        if obj.invoice_file:
            return format_html(f'<a href="{obj.invoice_file.url}" target="_blank">View Invoice</a>')
        return "No Invoice"

    invoice_link.short_description = 'Invoice'

    def has_add_permission(self, request):
        # Optionally prevent adding new orders through the admin
        return False

    def has_delete_permission(self, request, obj=None):
        # Optionally prevent deleting orders through the admin
        return False
