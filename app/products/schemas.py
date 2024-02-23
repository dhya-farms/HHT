from datetime import datetime
from typing import List, Optional

from _decimal import Decimal
from pydantic.v1 import BaseModel
from pydantic.v1 import condecimal, validator

from app.products.enums import DiscountType
from app.utils.helpers import allow_string_rep_of_enum


class CategoryCreateSchema(BaseModel):
    parent: Optional[int]
    name: str
    description: Optional[str] = None
    active: Optional[bool] = True


class CategoryUpdateSchema(BaseModel):
    parent: Optional[int]
    name: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = True


class CategoryListSchema(BaseModel):
    parent: Optional[int]
    name: Optional[str]
    active: Optional[bool]


class CollectionCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    active: Optional[bool] = True


class CollectionUpdateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    active: Optional[bool] = True


class CollectionListSchema(BaseModel):
    name: Optional[str]
    active: Optional[bool]


class SupplierCreateSchema(BaseModel):
    name: str
    company: Optional[str] = None
    phone_number: Optional[str] = None
    address_line1: Optional[str]
    address_line2: Optional[str] = None
    city: Optional[str] = None
    note: Optional[str] = None


class SupplierUpdateSchema(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    phone_number: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    note: Optional[str] = None


class SupplierListSchema(BaseModel):
    name: Optional[str]
    company: Optional[str]
    phone_number: Optional[str]
    city: Optional[str]


class TagCreateSchema(BaseModel):
    name: str


class TagUpdateSchema(BaseModel):
    name: Optional[str] = None


class TagListSchema(BaseModel):
    name: Optional[str]


class CouponCreateSchema(BaseModel):
    code: str
    discount_value: condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))
    discount_type: DiscountType
    max_usage: int
    valid_from: datetime
    valid_to: datetime
    active: Optional[bool] = True

    @validator('valid_from', 'valid_to', pre=True, allow_reuse=True)
    def validate_time(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"time format is incorrect: {e}")
        return v

    # Validator to allow string version of enum value too
    _validate_discount_type = validator('discount_type',
                                        allow_reuse=True,
                                        pre=True)(allow_string_rep_of_enum)


class CouponUpdateSchema(BaseModel):
    code: str
    discount_value: condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))
    discount_type: DiscountType
    max_usage: int
    valid_from: datetime
    valid_to: datetime
    active: Optional[bool] = True

    @validator('valid_from', 'valid_to', pre=True, allow_reuse=True)
    def validate_time(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"time format is incorrect: {e}")
        return v

    # Validator to allow string version of enum value too
    _validate_discount_type = validator('discount_type',
                                        allow_reuse=True,
                                        pre=True)(allow_string_rep_of_enum)


class CouponListSchema(BaseModel):
    code: Optional[str]
    discount_type: Optional[str]
    active: Optional[bool] = True


class ProductCreateSchema(BaseModel):
    slug: str
    name: str
    sku: Optional[str] = None
    buying_price = condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))
    sale_price = condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))
    short_description: str
    description: Optional[str]
    published: Optional[bool] = False
    note: Optional[str]
    collection_id: int


class ProductUpdateSchema(BaseModel):
    slug: str
    name: str
    sku: Optional[str] = None
    buying_price = condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))
    sale_price = condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))
    short_description: str
    description: Optional[str]
    published: Optional[bool] = False
    note: Optional[str]
    collection_id: int


class ProductListSchema(BaseModel):
    slug: Optional[str]
    name: Optional[str]
    sku: Optional[str]
    min_price = condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))
    max_price = condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))
    published: Optional[bool]
    collection_id: Optional[int]
    category_id: Optional[List[int]]
    tag_id: Optional[List[int]]
    supplier_id: Optional[List[int]]
    coupon_id: Optional[List[int]]


class ProductVariantCreateSchema(BaseModel):
    product_id: int
    sku: Optional[str] = None
    buying_price: condecimal(max_digits=10, decimal_places=2, ge=Decimal(0)) = None
    sale_price: condecimal(max_digits=10, decimal_places=2, ge=Decimal(0)) = None
    stock_quantity: Optional[int] = 0
    name: str
    short_description: str
    description: str
    published: Optional[bool] = False


class ProductVariantUpdateSchema(BaseModel):
    product_id: int
    sku: Optional[str] = None
    buying_price: condecimal(max_digits=10, decimal_places=2, ge=Decimal(0)) = None
    sale_price: condecimal(max_digits=10, decimal_places=2, ge=Decimal(0)) = None
    stock_quantity: Optional[int] = 0
    name: str
    short_description: str
    description: str
    published: Optional[bool] = False


class ProductVariantListSchema(BaseModel):
    product_id: Optional[int]


class ProductImageCreateSchema(BaseModel):
    product_id: Optional[int]
    product_variant_id: Optional[int]
    image: str
    is_thumbnail: Optional[bool] = False
    is_primary: Optional[bool] = False


class ProductImageUpdateSchema(BaseModel):
    product_id: Optional[int]
    product_variant_id: Optional[int] = None
    image: Optional[str] = None
    is_thumbnail: Optional[bool] = None
    is_primary: Optional[bool] = None


class ProductImageListSchema(BaseModel):
    product_id: Optional[int]
    product_variant_id: Optional[int]
    is_thumbnail: Optional[bool]
    is_primary: Optional[bool]


class AttributeCreateSchema(BaseModel):
    name: str


class AttributeUpdateSchema(BaseModel):
    name: Optional[str] = None


class AttributeListSchema(BaseModel):
    name: Optional[str]


class AttributeValueCreateSchema(BaseModel):
    attribute_id: int
    value: str


class AttributeValueUpdateSchema(BaseModel):
    attribute_id: int
    value: str


class AttributeValueListSchema(BaseModel):
    attribute_id: int
