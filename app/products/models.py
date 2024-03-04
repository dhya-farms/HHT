from django.db import models

from app.products.enums import DiscountType


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='sub_categories')
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to='merchandise/category_icons/', blank=True, null=True)
    image = models.ImageField(upload_to='merchandise/category_images/', blank=True, null=True)
    placeholder = models.ImageField(upload_to='merchandise/category_placeholders/', blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Collection(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to='merchandise/collection_icons/', blank=True, null=True)
    image = models.ImageField(upload_to='merchandise/collection_images/', blank=True, null=True)
    placeholder = models.ImageField(upload_to='merchandise/collection_placeholders/', blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    address_line1 = models.TextField(blank=True, null=True)
    address_line2 = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='merchandise/tag_icons/', blank=True, null=True)

    def __str__(self):
        return self.name


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    discount_type = models.IntegerField(choices=DiscountType.choices, default=DiscountType.PERCENTAGE)
    max_usage = models.IntegerField(help_text="Max number of times this coupon can be used")
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_to = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class Product(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=255, blank=True, null=True)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    short_description = models.CharField(max_length=165)
    description = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)
    collection = models.ForeignKey("products.Collection", on_delete=models.CASCADE, related_name='products')
    categories = models.ManyToManyField("products.Category", related_name='products')
    tags = models.ManyToManyField("products.Tag", related_name='tags')
    suppliers = models.ManyToManyField("products.Supplier", related_name='tags')
    coupons = models.ManyToManyField("products.Coupon", related_name='tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name='variants')
    attribute_values = models.ManyToManyField("products.AttributeValue", related_name='products')
    sku = models.CharField(max_length=45, blank=True, null=True)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock_quantity = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=165, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.name}"


class ProductImage(models.Model):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name='images', blank=True, null=True)
    product_variant = models.ForeignKey("products.ProductVariant", on_delete=models.CASCADE, related_name='images', blank=True, null=True)
    image = models.ImageField(upload_to='merchandise/product_images/', blank=True, null=True)
    placeholder = models.ImageField(upload_to='merchandise/product_placeholders/', blank=True, null=True)
    is_thumbnail = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_variant.name} Image"


class Attribute(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute = models.ForeignKey("products.Attribute", on_delete=models.CASCADE, related_name='attribute_values')
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"
