from django.contrib import admin
from app.payments.models import Payment, Return, Refund, ReturnItem
from django.utils.html import format_html
from django.urls import reverse


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'order', 'amount', 'payment_method_display', 'payment_status_display', 'transaction_id', 'created_at')
    list_filter = ('payment_method', 'payment_status', 'created_at')
    search_fields = ('order__id', 'transaction_id')
    date_hierarchy = 'created_at'

    def payment_method_display(self, obj):
        return obj.get_payment_method_display()

    payment_method_display.admin_order_field = 'payment_method'
    payment_method_display.short_description = 'Payment Method'

    def payment_status_display(self, obj):
        return obj.get_payment_status_display()

    payment_status_display.admin_order_field = 'payment_status'
    payment_status_display.short_description = 'Payment Status'


@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'reason', 'status_display', 'created_at', 'view_return_items_link')
    list_filter = ('status', 'created_at')
    search_fields = ('order__id', 'reason')
    date_hierarchy = 'created_at'

    def status_display(self, obj):
        return obj.get_status_display()

    status_display.admin_order_field = 'status'
    status_display.short_description = 'Status'

    def view_return_items_link(self, obj):
        url = (
            reverse("admin:app_returnitem_changelist")
            + "?"
            + "return_obj__id__exact={}".format(obj.pk)
        )
        return format_html('<a href="{}">View Return Items</a>', url)

    view_return_items_link.short_description = "Return Items"


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'payment', 'return_obj', 'refund_type_display', 'amount', 'reason', 'status_display', 'created_at')
    list_filter = ('refund_type', 'status', 'created_at')
    search_fields = ('payment__id', 'return_obj__id', 'reason')
    date_hierarchy = 'created_at'

    def refund_type_display(self, obj):
        return obj.get_refund_type_display()

    refund_type_display.admin_order_field = 'refund_type'
    refund_type_display.short_description = 'Refund Type'

    def status_display(self, obj):
        return obj.get_status_display()

    status_display.admin_order_field = 'status'
    status_display.short_description = 'Status'


@admin.register(ReturnItem)
class ReturnItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'return_obj', 'product_variant', 'quantity', 'created_at')
    list_filter = ('return_obj', 'product_variant')
    search_fields = ('return_obj__id', 'product_variant__name')
    date_hierarchy = 'created_at'
