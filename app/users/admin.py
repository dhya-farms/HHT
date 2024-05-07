from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
from ..customers.admin import AddressInline, ReviewInline


class CustomUserAdmin(UserAdmin):
    model = User
    inlines = [AddressInline, ReviewInline]  # Ensure these inline models are defined or imported appropriately
    list_display = ('id', 'name', 'email', 'mobile_no', 'user_type', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active', 'user_type',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'mobile_no', 'user_type')}),
        (_('Personal info'), {'fields': ('favorites',)}),  # Added favorites under Personal info
        (_('Permissions'), {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'mobile_no', 'user_type', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email', 'name', 'mobile_no',)
    ordering = ('email',)


# Register the updated admin model
admin.site.register(User, CustomUserAdmin)
