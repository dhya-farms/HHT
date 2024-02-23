from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.users.models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'name', 'email', 'mobile_no', 'role', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active', 'role',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'mobile_no', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'mobile_no', 'role', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email', 'name', 'mobile_no',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
