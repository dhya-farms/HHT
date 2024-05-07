from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from app.users.models import User
from app.customers.admin import AddressInline, ReviewInline  # Ensure these are defined or imported appropriately


class CustomUserAdmin(UserAdmin):
    model = User
    inlines = [AddressInline, ReviewInline]  # Inline admin views for related models
    list_display = ('id', 'username', 'name', 'email', 'mobile_no', 'user_type', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active', 'user_type',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'name', 'mobile_no', 'user_type')}),
        (_('Personal info'), {'fields': ('favorites',)}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'username', 'email', 'password1', 'password2', 'name', 'mobile_no', 'user_type', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('username', 'email', 'name', 'mobile_no',)
    ordering = ('email', 'username',)  # Added username to ordering for better admin interface usability


# Register the updated admin model
admin.site.register(User, CustomUserAdmin)
