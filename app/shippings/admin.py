from django.contrib import admin
from app.shippings.models import ShippingProvider, Shipment, DeliveryStatus, ShippingRate, PincodeAvailability


@admin.register(ShippingProvider)
class ShippingProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'tracking_url_template', 'api_endpoint', 'api_key')
    search_fields = ('name',)


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = (
        'order', 'provider', 'tracking_number', 'shipped_date', 'estimated_delivery_date', 'actual_delivery_date',
        'status_display')
    list_filter = ('status', 'provider', 'shipped_date')
    search_fields = ('order__id', 'tracking_number')
    date_hierarchy = 'shipped_date'

    def status_display(self, obj):
        return obj.get_status_display()

    status_display.admin_order_field = 'status'
    status_display.short_description = 'Status'


@admin.register(DeliveryStatus)
class DeliveryStatusAdmin(admin.ModelAdmin):
    list_display = ('shipment', 'status_display', 'status_date', 'location', 'notes')
    list_filter = ('status', 'shipment')
    search_fields = ('shipment__tracking_number', 'location')
    date_hierarchy = 'status_date'

    def status_display(self, obj):
        return obj.get_status_display()

    status_display.admin_order_field = 'status'
    status_display.short_description = 'Status'


@admin.register(ShippingRate)
class ShippingRateAdmin(admin.ModelAdmin):
    list_display = ['pincode', 'rate', 'estimated_delivery_days']
    search_fields = ['pincode']


@admin.register(PincodeAvailability)
class PincodeAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['pincode', 'is_available']
    search_fields = ['pincode']
