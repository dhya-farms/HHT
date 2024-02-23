from rest_framework import serializers

from app.users.enums import Role
from app.users.models import User
from app.utils.helpers import get_serialized_enum


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=Role.choices)

    class Meta:
        model = User
        fields = ['id', 'name', 'mobile_no', 'role', 'created_at', 'updated_at', 'email',
                  'is_active', 'last_login', 'date_joined']

    def get_role(self, obj):
        if obj.role:
            return get_serialized_enum(Role(obj.role))
        return dict()
