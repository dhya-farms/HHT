from django.core.cache import cache
from django.http import JsonResponse
from rest_framework import viewsets, status
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, OpenApiResponse
from rest_framework.decorators import action
from rest_framework.response import Response

from .controllers import CategoryController, CollectionController, SupplierController, TagController, CouponController, \
    ProductController, ProductVariantController, ProductImageController, AttributeValueController, AttributeController
from .models import ProductImage
from .serializers import CategorySerializer, CollectionSerializer, SupplierSerializer, TagSerializer, CouponSerializer, \
    ProductSerializer, ProductVariantSerializer, ProductImageSerializer, AttributeValueSerializer, AttributeSerializer
from .schemas import CategoryCreateSchema, CategoryUpdateSchema, CategoryListSchema, CollectionCreateSchema, \
    CollectionUpdateSchema, CollectionListSchema, SupplierCreateSchema, SupplierUpdateSchema, SupplierListSchema, \
    TagCreateSchema, TagUpdateSchema, TagListSchema, CouponCreateSchema, CouponUpdateSchema, CouponListSchema, \
    ProductCreateSchema, ProductUpdateSchema, ProductListSchema, ProductVariantCreateSchema, ProductVariantUpdateSchema, \
    ProductVariantListSchema, ProductImageCreateSchema, ProductImageUpdateSchema, ProductImageListSchema, \
    AttributeValueCreateSchema, AttributeValueUpdateSchema, AttributeValueListSchema, AttributeCreateSchema, \
    AttributeUpdateSchema, AttributeListSchema
from ..utils.constants import CacheKeys, Timeouts
from ..utils.pagination import CustomPageNumberPagination
from ..utils.views import BaseViewSet


class CategoryViewSet(BaseViewSet):
    controller = CategoryController()
    serializer = CategorySerializer
    create_schema = CategoryCreateSchema
    update_schema = CategoryUpdateSchema
    list_schema = CategoryListSchema
    cache_key_retrieve = CacheKeys.CATEGORY_DETAILS_BY_PK
    cache_key_list = CacheKeys.CATEGORY_LIST

    @extend_schema(
        description="Create a new Category",
        request=CategoryCreateSchema,
        responses={201: CategorySerializer},
        examples=[
            OpenApiExample(
                name="Create Category Example",
                description="Example payload for creating a new category.",
                value={
                    "parent": 1,
                    "name": "New Category Name",
                    "description": "Description of the new category",
                    "active": True
                },
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Partially update an existing Category",
        request=CategoryUpdateSchema,
        responses={200: CategorySerializer},
        examples=[
            OpenApiExample(
                name="Update Category Example",
                description="Example payload for partially updating an existing category.",
                value={
                    "name": "Updated Category Name",
                    "description": "Updated description of the category",
                },
            ),
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List and filter Categories",
        responses={200: CategorySerializer(many=True)},
        parameters=[
            OpenApiParameter(name='parent', type=int),
            OpenApiParameter(name='name', type=str),
            OpenApiParameter(name='active', type=bool)]

    )
    def list(self, request, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific Category lead by id",
        parameters=[
            OpenApiParameter(
                name='pk',
                location=OpenApiParameter.PATH,
                required=True, type=int,
                description='Category'),
        ],
        responses={200: CategorySerializer}
    )
    def retrieve(self, request, pk, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)

    @extend_schema(
        description="Make a Category inactive",
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, required=True, type=int, description='CRM'),
        ],
        responses={200: OpenApiResponse(description="Category inactivated successfully")}
    )
    @action(methods=['post'], detail=True, url_path='make-inactive')
    def make_inactive(self, request, pk, *args, **kwargs):
        return super().make_inactive(request, pk, *args, **kwargs)


class CollectionViewSet(BaseViewSet):
    controller = CollectionController()  # Replace with your actual controller
    serializer = CollectionSerializer  # Replace with your actual serializer
    create_schema = CollectionCreateSchema
    update_schema = CollectionUpdateSchema
    list_schema = CollectionListSchema
    cache_key_retrieve = CacheKeys.COLLECTION_DETAILS_BY_PK  # Update as needed
    cache_key_list = CacheKeys.COLLECTION_LIST  # Update as needed

    @extend_schema(
        description="Create a new Collection",
        request=CollectionCreateSchema,
        responses={201: CollectionSerializer},
        examples=[
            OpenApiExample(
                name="Create Collection Example",
                description="Example payload for creating a new collection.",
                value={
                    "name": "Spring Collection",
                    "description": "A vibrant collection for the spring season",
                    "active": True
                },
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing Collection",
        request=CollectionUpdateSchema,
        responses={200: CollectionSerializer},
        examples=[
            OpenApiExample(
                name="Update Collection Example",
                description="Example payload for updating an existing collection.",
                value={
                    "name": "Summer Collection",
                    "description": "An updated description for the summer collection",
                    "active": True
                },
            ),
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        description="List all Collections",
        responses={200: CollectionSerializer(many=True)},
        parameters=[
            OpenApiParameter(name='name', type=str, description='Filter by collection name'),
            OpenApiParameter(name='active', type=bool, description='Filter by active status')
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific Collection by ID",
        responses={200: CollectionSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)

    @extend_schema(
        description="Retrieve a specific collection by id",
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, required=True, type=int,
                             description='collection ID'),
        ],
        responses={200: CollectionSerializer}
    )
    def retrieve(self, request, pk, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)


class SupplierViewSet(BaseViewSet):
    controller = SupplierController()
    serializer = SupplierSerializer
    create_schema = SupplierCreateSchema
    update_schema = SupplierUpdateSchema
    list_schema = SupplierListSchema
    cache_key_retrieve = CacheKeys.SUPPLIER_DETAILS_BY_PK
    cache_key_list = CacheKeys.SUPPLIER_LIST

    @extend_schema(
        description="Create a new Supplier",
        request=SupplierCreateSchema,
        responses={201: SupplierSerializer},
        examples=[
            OpenApiExample(
                name="Create Supplier Example",
                description="Example payload for creating a new supplier.",
                value={
                    "name": "Supplier Name",
                    "company": "Supplier Company",
                    "phone_number": "1234567890",
                    "address_line1": "123 Main St",
                    "address_line2": "Suite 100",
                    "city": "City",
                    "note": "Notes about the supplier"
                },
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Partially update an existing Supplier",
        request=SupplierUpdateSchema,
        responses={200: SupplierSerializer},
        examples=[
            OpenApiExample(
                name="Update Supplier Example",
                description="Example payload for updating an existing supplier.",
                value={
                    "name": "Updated Supplier Name",
                    "company": "Updated Company",
                    "phone_number": "0987654321",
                    "address_line1": "456 Main St",
                    "address_line2": "Suite 101",
                    "city": "New City",
                    "note": "Updated notes about the supplier"
                },
            ),
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List all Suppliers",
        responses={200: SupplierSerializer(many=True)},
        parameters=[
            OpenApiParameter(name='name', type=str, description='Filter by supplier name'),
            OpenApiParameter(name='company', type=str, description='Filter by company name'),
            OpenApiParameter(name='phone_number', type=str, description='Filter by phone number'),
            OpenApiParameter(name='city', type=str, description='Filter by city'),
        ]
    )
    def list(self, request, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific Supplier by id",
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, required=True, type=int, description='CRM '
                                                                                                             'Lead ID'),
        ],
        responses={200: SupplierSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)

    @extend_schema(
        description="Make a Supplier inactive",
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, required=True, type=int, description='CRM '
                                                                                                             'Lead ID'),
        ],
        responses={200: OpenApiResponse(description="Supplier inactivated successfully")}
    )
    @action(methods=['POST'], detail=True)
    def make_inactive(self, request, pk, *args, **kwargs):
        return super().make_inactive(request, pk, *args, **kwargs)


class TagViewSet(BaseViewSet):
    controller = TagController()
    serializer = TagSerializer
    create_schema = TagCreateSchema
    update_schema = TagUpdateSchema
    list_schema = TagListSchema
    cache_key_retrieve = CacheKeys.TAG_DETAILS_BY_PK
    cache_key_list = CacheKeys.TAG_LIST

    @extend_schema(
        description="Create a new Tag",
        request=TagCreateSchema,
        responses={201: TagSerializer},
        examples=[
            OpenApiExample(
                name="Create Tag Example",
                description="Example payload for creating a new tag.",
                value={"name": "New Tag"}
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing Tag",
        request=TagUpdateSchema,
        responses={200: TagSerializer},
        examples=[
            OpenApiExample(
                name="Update Tag Example",
                description="Example payload for updating an existing tag.",
                value={"name": "Updated Tag Name"}
            ),
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        description="List all Tags",
        responses={200: TagSerializer(many=True)},
        parameters=[
            OpenApiParameter(name='name', description='Filter tags by name', required=False, type=str)
        ]
    )
    def list(self, request, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific Tag by ID",
        responses={200: TagSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)

    @extend_schema(
        description="Make a Tag inactive",
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, required=True, type=int, description='CRM '
                                                                                                             'Lead ID'),
        ],
        responses={200: OpenApiResponse(description="Tag inactivated successfully")}
    )
    @action(methods=['POST'], detail=True)
    def make_inactive(self, request, pk, *args, **kwargs):
        return super().make_inactive(request, pk, *args, **kwargs)


class CouponViewSet(BaseViewSet):
    controller = CouponController()
    serializer = CouponSerializer
    create_schema = CouponCreateSchema
    update_schema = CouponUpdateSchema
    list_schema = CouponListSchema
    cache_key_retrieve = CacheKeys.COUPON_DETAILS_BY_PK
    cache_key_list = CacheKeys.COUPON_LIST

    @extend_schema(
        description="Create a new Coupon",
        request=CouponCreateSchema,
        responses={201: CouponSerializer},
        examples=[
            OpenApiExample(
                name="Coupon Creation Example",
                value={
                    "code": "DISCOUNT20",
                    "discount_value": 20,
                    "discount_type": 1,  # Assuming 1 = Percentage, for example
                    "max_usage": 100,
                    "valid_from": "2024-01-01T00:00:00Z",
                    "valid_to": "2024-12-31T23:59:59Z",
                    "active": True
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Partially update an existing Coupon",
        request=CouponUpdateSchema,
        responses={200: CouponSerializer},
        examples=[
            OpenApiExample(
                name="Coupon Update Example",
                value={
                    "code": "SUMMER21",
                    "discount_value": 15,
                    "discount_type": 1,
                    "max_usage": 200,
                    "valid_from": "2024-06-01T00:00:00Z",
                    "valid_to": "2024-08-31T23:59:59Z",
                    "active": True
                }
            )
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        description="List and filter Coupons",
        responses={200: CouponSerializer(many=True)},
        parameters=[
            OpenApiParameter(name="code", type=str, description="Filter by coupon code"),
            OpenApiParameter(name="discount_type", type=str, description="Filter by discount type"),
            OpenApiParameter(name="active", type=bool, description="Filter by active status")
        ]
    )
    def list(self, request, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific Coupon by ID",
        responses={200: CouponSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)


class ProductViewSet(BaseViewSet):
    serializer = ProductSerializer
    controller = ProductController()
    create_schema = ProductCreateSchema
    update_schema = ProductUpdateSchema
    list_schema = ProductListSchema
    cache_key_retrieve = CacheKeys.PRODUCT_DETAILS_BY_SLUG
    cache_key_list = CacheKeys.PRODUCT_LIST
    lookup_field = 'slug'

    @extend_schema(
        description="Create a new Product",
        request=ProductCreateSchema,
        responses={201: ProductSerializer},
        examples=[
            OpenApiExample(
                name="Create Product Example",
                value={
                    "slug": "new-product",
                    "name": "New Product Name",
                    "sku": "SKU12345",
                    "buying_price": 50.00,
                    "sale_price": 70.00,
                    "short_description": "Short description of the product",
                    "description": "Detailed description of the product",
                    "published": True,
                    "note": "Some notes about the product",
                    "collection_id": 1
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Partially update an existing Product",
        request=ProductUpdateSchema,
        responses={200: ProductSerializer},
        examples=[
            OpenApiExample(
                name="Update Product Example",
                value={
                    "slug": "updated-product",
                    "name": "Updated Product Name",
                    "sku": "SKU54321",
                    "buying_price": 60.00,
                    "sale_price": 80.00,
                    "short_description": "Updated short description of the product",
                    "description": "Updated detailed description of the product",
                    "published": False,
                    "note": "Updated notes about the product",
                    "collection_id": 2
                }
            )
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        description="List and filter Products",
        responses={200: ProductSerializer(many=True)},
        parameters=[
            OpenApiParameter(name="slug", type=str, description="Filter by product slug"),
            OpenApiParameter(name="name", type=str, description="Filter by product name"),
            OpenApiParameter(name="sku", type=str, description="Filter by product SKU"),
            OpenApiParameter(name="min_price", type=str, description="Filter by product price"),
            OpenApiParameter(name="max_price", type=str, description="Filter by product price"),
            OpenApiParameter(name="published", type=bool, description="Filter by published status"),
            OpenApiParameter(name="collection_id", type=int, description="Filter by collection ID"),
            OpenApiParameter(name="category_id", type=int, description="Filter by categories IDs"),
            OpenApiParameter(name="tag_id", type=int, description="Filter by tags IDs"),
            OpenApiParameter(name="supplier_id", type=int, description="Filter by suppliers IDs"),
            OpenApiParameter(name="coupon_id", type=int, description="Filter by coupons IDs"),
            OpenApiParameter(name="ordering", type=str, description="sort by ordering"),
        ]
    )
    def list(self, request, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific Product by Slug",
        responses={200: ProductSerializer}
    )
    def retrieve(self, request, *args, slug=None):
        instance, cache_key = None, ""
        if self.cache_key_retrieve.value:
            cache_key = self.cache_key_retrieve.value.format(slug=slug)
            instance = cache.get(cache_key)
        if instance:
            data = instance
        else:
            instance = self.controller.get_product_by_slug(slug=slug)
            if not instance:
                return JsonResponse({"error": "Instance with this slug does not exist"}, status=status.HTTP_404_NOT_FOUND)
            data = self.controller.serialize_one(instance, self.serializer)
            if self.cache_key_retrieve:
                cache.set(cache_key, data, timeout=Timeouts.MINUTES_10)
        return JsonResponse(data=data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='add-to-favorites')
    def add_to_favorites(self, request, slug=None):
        product = self.controller.get_product_by_slug(slug=slug)
        if not product:
            return JsonResponse({"error": "Product with this ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        request.user.favorites.add(product)
        return JsonResponse({'status': 'product added to favorites'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='remove-from-favorites')
    def remove_from_favorites(self, request, slug=None):
        product = self.controller.get_product_by_slug(slug=slug)
        if not product:
            return JsonResponse({"error": "Product with this ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        request.user.favorites.remove(product)
        return JsonResponse({'status': 'product removed from favorites'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='my-favourites')
    def list_favorites(self, request):
        paginator = CustomPageNumberPagination()
        queryset = request.user.favorites.all()
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            res = self.controller.serialize_queryset(page, self.serializer)
            return paginator.get_paginated_response(res)
        res = self.controller.serialize_queryset(queryset, self.serializer)
        return JsonResponse(res, safe=False, status=status.HTTP_200_OK)


class ProductVariantViewSet(BaseViewSet):
    serializer = ProductVariantSerializer
    controller = ProductVariantController()
    create_schema = ProductVariantCreateSchema
    update_schema = ProductVariantUpdateSchema
    list_schema = ProductVariantListSchema
    cache_key_retrieve = CacheKeys.PRODUCT_VARIANT_DETAILS_BY_PK
    cache_key_list = CacheKeys.PRODUCT_VARIANT_LIST

    @extend_schema(
        description="Create a new Product Variant",
        request=ProductVariantCreateSchema,
        responses={201: ProductVariantSerializer},
        examples=[
            OpenApiExample(
                name="Create Product Variant Example",
                value={
                    "product_id": 1,
                    "sku": "VARIANT123",
                    "buying_price": 50.00,
                    "sale_price": 70.00,
                    "stock_quantity": 100,
                    "name": "Variant Name",
                    "short_description": "Short description of the variant",
                    "description": "Detailed description of the variant",
                    "published": True
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing Product Variant",
        request=ProductVariantUpdateSchema,
        responses={200: ProductVariantSerializer},
        examples=[
            OpenApiExample(
                name="Update Product Variant Example",
                value={
                    "product_id": 1,
                    "sku": "VARIANT321",
                    "buying_price": 60.00,
                    "sale_price": 80.00,
                    "stock_quantity": 200,
                    "name": "Updated Variant Name",
                    "short_description": "Updated short description",
                    "description": "Updated detailed description",
                    "published": False
                }
            )
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        description="List and filter Product Variants",
        responses={200: ProductVariantSerializer(many=True)},
        parameters=[
            OpenApiParameter(name="product_id", type=int, description="Filter by product ID"),
        ]
    )
    def list(self, request, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific Product Variant by ID",
        responses={200: ProductVariantSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)

    @extend_schema(
        description="Add this Product Variant to Cart)",
        methods=['POST'],
        responses={200: OpenApiResponse(description="Added to Cart Successfully")}
    )
    @action(detail=True, methods=['post'], url_path='add-to-cart')
    def add_to_cart(self, request, pk, *args, **kwargs):
        errors, instance = self.controller.add_to_cart(pk, request.user)
        if errors:
            return JsonResponse(data=errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Added to Cart Successfully"}, status=status.HTTP_200_OK)

    @extend_schema(
        description="Remove this Product Variant to Cart",
        methods=['POST'],
        responses={200: OpenApiResponse(description="Removed from Cart Successfully")}
    )
    @action(detail=True, methods=['post'], url_path='remove-from-cart')
    def remove_from_cart(self, request, pk, *args, **kwargs):
        errors, instance = self.controller.remove_from_cart(pk, request.user)
        if errors:
            return JsonResponse(data=errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Removed from Cart Successfully"}, status=status.HTTP_200_OK)

    @extend_schema(
        description="Increase the count of this Product Variant to Cart",
        methods=['POST'],
        responses={200: OpenApiResponse(description="Increased Cart Item successfully")}
    )
    @action(detail=True, methods=['post'], url_path='increase-cart-item')
    def increase_cart_item(self, request, pk, *args, **kwargs):
        errors, instance = self.controller.increase_cart_item(pk, request.user)
        if errors:
            return JsonResponse(data=errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Increased Cart Item Successfully"}, status=status.HTTP_200_OK)

    @extend_schema(
        description="Decrease the count of this Product Variant to Cart",
        methods=['POST'],
        responses={200: OpenApiResponse(description="Decreased Cart Item successfully")}
    )
    @action(detail=True, methods=['post'], url_path='decrease-cart-item')
    def decrease_cart_item(self, request, pk, *args, **kwargs):
        errors, instance = self.controller.decrease_cart_item(pk, request.user)
        if errors:
            return JsonResponse(data=errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Decreased Cart Item Successfully"}, status=status.HTTP_200_OK)


class ProductImageViewSet(BaseViewSet):
    queryset = ProductImage.objects.all()
    serializer = ProductImageSerializer
    controller = ProductImageController()
    create_schema = ProductImageCreateSchema
    update_schema = ProductImageUpdateSchema
    list_schema = ProductImageListSchema
    cache_key_retrieve = CacheKeys.PRODUCT_IMAGE_DETAILS_BY_PK
    cache_key_list = CacheKeys.PRODUCT_IMAGE_LIST

    @extend_schema(
        description="Create a new Product Image",
        request=ProductImageCreateSchema,
        responses={201: ProductImageSerializer},
        examples=[
            OpenApiExample(
                name="Create Product Image Example",
                value={
                    "product_id": 1,
                    "product_variant_id": 1,
                    "image": "url/to/image",
                    "is_thumbnail": True,
                    "is_primary": False
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing Product Image",
        request=ProductImageUpdateSchema,
        responses={200: ProductImageSerializer},
        examples=[
            OpenApiExample(
                name="Update Product Image Example",
                value={
                    "product_id": 1,
                    "product_variant_id": 1,
                    "image": "url/to/updated/image",
                    "is_thumbnail": False,
                    "is_primary": True
                }
            )
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        description="List and filter Product Images",
        responses={200: ProductImageSerializer(many=True)},
        parameters=[
            OpenApiParameter(name="product_id", type=int, description="Filter by product ID"),
            OpenApiParameter(name="product_variant_id", type=int, description="Filter by product variant ID"),
            OpenApiParameter(name="is_thumbnail", type=bool, description="Filter by thumbnail status"),
            OpenApiParameter(name="is_primary", type=bool, description="Filter by primary status")
        ]
    )
    def list(self, request, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific Product Image by ID",
        responses={200: ProductImageSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)


class AttributeViewSet(BaseViewSet):
    serializer = AttributeSerializer
    controller = AttributeController()
    create_schema = AttributeCreateSchema
    update_schema = AttributeUpdateSchema
    list_schema = AttributeListSchema
    cache_key_retrieve = CacheKeys.ATTRIBUTE_DETAILS_BY_PK
    cache_key_list = CacheKeys.ATTRIBUTE_LIST

    @extend_schema(
        description="Create a new Attribute",
        request=AttributeCreateSchema,
        responses={201: AttributeSerializer},
        examples=[
            OpenApiExample(
                name="Create Attribute Example",
                value={"name": "Color"}
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing Attribute",
        request=AttributeUpdateSchema,
        responses={200: AttributeSerializer},
        examples=[
            OpenApiExample(
                name="Update Attribute Example",
                value={"name": "Size"}
            )
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        description="List and filter Attributes",
        responses={200: AttributeSerializer(many=True)},
        parameters=[
            OpenApiParameter(name="name", type=str, description="Filter by attribute name")
        ]
    )
    def list(self, request, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific Attribute by ID",
        responses={200: AttributeSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)


class AttributeValueViewSet(BaseViewSet):
    serializer = AttributeValueSerializer
    controller = AttributeValueController()
    create_schema = AttributeValueCreateSchema
    update_schema = AttributeValueUpdateSchema
    list_schema = AttributeValueListSchema
    cache_key_retrieve = CacheKeys.ATTRIBUTE_VALUE_DETAILS_BY_PK
    cache_key_list = CacheKeys.ATTRIBUTE_VALUE_LIST

    @extend_schema(
        description="Create a new Attribute Value",
        request=AttributeValueCreateSchema,
        responses={201: AttributeValueSerializer},
        examples=[
            OpenApiExample(
                name="Create Attribute Value Example",
                value={
                    "attribute_id": 1,
                    "value": "Red"
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Update an existing Attribute Value",
        request=AttributeValueUpdateSchema,
        responses={200: AttributeValueSerializer},
        examples=[
            OpenApiExample(
                name="Update Attribute Value Example",
                value={
                    "attribute_id": 1,
                    "value": "Blue"
                }
            )
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        description="List and filter Attribute Values",
        responses={200: AttributeValueSerializer(many=True)},
        parameters=[
            OpenApiParameter(name="attribute_id", type=int, description="Filter by attribute ID")
        ]
    )
    def list(self, request, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific Attribute Value by ID",
        responses={200: AttributeValueSerializer}
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)
