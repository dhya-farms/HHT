from django.db import models
from django.db.models import Q
from psycopg import IntegrityError

from app.customers.models import CartItem
from app.products.models import Category, Collection, Supplier, Tag, Coupon, Product, ProductVariant, ProductImage, \
    Attribute, AttributeValue
from app.utils.controllers import Controller
from app.utils.helpers import get_serialized_exception


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

    def filter(self,
               slug,
               name,
               sku,
               min_price,
               max_price,
               published,
               collection_id,
               category_id,
               tag_id,
               supplier_id,
               coupon_id,
               ordering):
        try:
            queries = Q()

            if slug:
                queries &= Q(slug=slug)
            if name:
                queries &= Q(name__icontains=name)
            if sku:
                queries &= Q(sku=sku)
            if min_price:
                queries &= Q(sale_price__gte=min_price)
            if max_price:
                queries &= Q(sale_price__lte=max_price)
            if published is not None:
                queries &= Q(published=published)
            if collection_id:
                queries &= Q(collection_id=collection_id)
            if category_id:
                queries &= Q(categories__id__in=category_id)
            if tag_id:
                queries &= Q(tags__id__in=tag_id)
            if supplier_id:
                queries &= Q(suppliers__id__in=supplier_id)
            if coupon_id:
                queries &= Q(coupons__id__in=coupon_id)

            return None, self.model.objects.filter(queries).distinct().order_by(ordering)
        except Exception as e:
            return get_serialized_exception(e)

    def get_product_by_slug(self, slug):
        product = self.get_valid_qs().filter(slug=slug).first()
        if product:
            return product
        else:
            return None

    def get_valid_qs(self):
        return self.model.objects.filter(published=True)


class ProductVariantController(Controller):
    def __init__(self):
        super().__init__(model=ProductVariant)

    def add_to_cart(self, pk, user):
        try:
            product_variant: ProductVariant = self.model.objects.get(pk=pk)
            cart_item, item_created = CartItem.objects.get_or_create(user=user,
                                                                     product_variant=product_variant)

            return None, cart_item
        except (IntegrityError, ValueError) as e:
            return get_serialized_exception(e)

    def remove_from_cart(self, pk, user):
        try:
            product_variant: ProductVariant = self.model.objects.get(pk=pk)
            try:
                cart_item = CartItem.objects.get(user=user, product_variant=product_variant)
                if cart_item.quantity >= 1:
                    cart_item.delete()
            except CartItem.DoesNotExist:
                pass
            return None, True
        except (IntegrityError, ValueError) as e:
            return get_serialized_exception(e)

    def increase_cart_item(self, pk, user):
        try:
            product_variant: ProductVariant = self.model.objects.get(pk=pk)
            cart_item, item_created = CartItem.objects.get_or_create(user=user,
                                                                     product_variant=product_variant)

            if not item_created:
                cart_item.quantity += 1
                cart_item.save()
            else:
                pass
            return None, cart_item
        except (IntegrityError, ValueError) as e:
            return get_serialized_exception(e)

    def decrease_cart_item(self, pk, user):
        try:
            product_variant: ProductVariant = self.model.objects.get(pk=pk)
            cart_item = CartItem.objects.get_or_create(user=user,
                                                       product_variant=product_variant)

            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
            return None, cart_item
        except (IntegrityError, ValueError) as e:
            return get_serialized_exception(e)


class ProductImageController(Controller):
    def __init__(self):
        super().__init__(model=ProductImage)


class AttributeController(Controller):
    def __init__(self):
        super().__init__(model=Attribute)


class AttributeValueController(Controller):
    def __init__(self):
        super().__init__(model=AttributeValue)
