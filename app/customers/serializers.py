from rest_framework import serializers

from app.customers.enums import AddressType
from app.customers.models import Customer, Address, Wishlist, WishlistItem, Review, CartItem
from app.products.serializers import ProductVariantSerializer, \
    ProductSerializer
from app.users.serializers import UserSerializer
from app.utils.helpers import get_serialized_enum


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    # address_type = serializers.SerializerMethodField()
    #
    # def get_address_type(self, obj):
    #     return get_serialized_enum(AddressType(obj.address_type))

    class Meta:
        model = Address
        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'


class WishlistItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = WishlistItem
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product_variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'
