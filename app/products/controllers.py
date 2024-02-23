from django.db import models

from app.products.models import Category, Collection, Supplier, Tag, Coupon, Product, ProductVariant, ProductImage, \
    Attribute, AttributeValue
from app.utils.controllers import Controller


class CategoryController(Controller):
    def __init__(self):
        super().__init__(model=Category)


class CollectionController(Controller):
    def __init__(self):
        super().__init__(model=Collection)


class SupplierController(Controller):
    def __init__(self):
        super().__init__(model=Supplier)


class TagController(Controller):
    def __init__(self):
        super().__init__(model=Tag)


class CouponController(Controller):
    def __init__(self):
        super().__init__(model=Coupon)


class ProductController(Controller):
    def __init__(self):
        super().__init__(model=Product)


class ProductVariantController(Controller):
    def __init__(self):
        super().__init__(model=ProductVariant)


class ProductImageController(Controller):
    def __init__(self):
        super().__init__(model=ProductImage)


class AttributeController(Controller):
    def __init__(self):
        super().__init__(model=Attribute)


class AttributeValueController(Controller):
    def __init__(self):
        super().__init__(model=AttributeValue)
