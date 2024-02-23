from django.contrib import admin
from app.products.models import Category, Collection, Supplier, Tag, Coupon, Product, ProductVariant, ProductImage, \
    Attribute, AttributeValue


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'active', 'created_at')
    list_filter = ('active', 'parent')
    search_fields = ('name',)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'created_at')
    list_filter = ('active',)
    search_fields = ('name',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'phone_number', 'city', 'created_at')
    list_filter = ('city',)
    search_fields = ('name', 'company', 'phone_number')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'max_usage', 'valid_from', 'valid_to', 'active')
    list_filter = ('active', 'discount_type')
    search_fields = ('code',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'collection', 'published', 'created_at')
    list_filter = ('published', 'collection')
    search_fields = ('name', 'slug')
    inlines = [ProductVariantInline, ProductImageInline]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'sku', 'stock_quantity', 'published')
    list_filter = ('published', 'product')
    search_fields = ('name', 'sku')
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'product_variant', 'is_thumbnail', 'is_primary')
    list_filter = ('is_thumbnail', 'is_primary')


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    inlines = [AttributeValueInline]


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'value')
    list_filter = ('attribute',)
    search_fields = ('value',)
