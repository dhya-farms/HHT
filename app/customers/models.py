from django.db import models

from app.customers.enums import AddressType
from app.users.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Address(models.Model):
    user = models.ForeignKey("users.User", blank=True, null=True, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.IntegerField(choices=AddressType.choices)
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f"{AddressType(self.address_type).value} Address: {self.line1}, {self.city}, {self.pincode}"


class Wishlist(models.Model):
    user = models.ForeignKey("users.User",  blank=True, null=True, on_delete=models.CASCADE, related_name='wishlists')
    name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or f"Wishlist {self.id}"


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey('products.ProductVariant', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_variant.name} in {self.wishlist.name or 'Wishlist'}"


class Review(models.Model):
    user = models.ForeignKey("users.User",  blank=True, null=True, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"


class CartItem(models.Model):
    user = models.ForeignKey("users.User",  blank=True, null=True, on_delete=models.CASCADE, related_name='cart_items')
    product_variant = models.ForeignKey('products.ProductVariant', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product_variant.name}"
