from rest_framework import serializers

from app.users.enums import UserType
from app.users.models import User
from app.utils.helpers import get_serialized_enum


class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'mobile_no', 'user_type', 'created_at', 'updated_at', 'email',
                  'is_active', 'last_login', 'date_joined']

    def get_user_type(self, obj):
        if obj.user_type:
            return get_serialized_enum(UserType(obj.user_type))
        return dict()
