from _decimal import Decimal
from pydantic.v1 import BaseModel, validator, condecimal
from typing import Optional

from app.customers.enums import AddressType
from app.utils.helpers import allow_string_rep_of_enum, convert_to_decimal


# Customer Schemas
class CustomerCreateSchema(BaseModel):
    user_id: int


class CustomerUpdateSchema(BaseModel):
    user_id: int


class CustomerListSchema(BaseModel):
    user_id: int


# Address Schemas
class AddressCreateSchema(BaseModel):
    user_id: int
    address_type: AddressType
    line1: str
    line2: Optional[str]
    city: Optional[str]
    pincode: str

    # Validator to allow string version of enum value too
    _validate_address_type = validator('address_type',
                                       allow_reuse=True,
                                       pre=True)(allow_string_rep_of_enum)


class AddressUpdateSchema(BaseModel):
    user_id: int
    address_type: AddressType
    line1: str
    line2: Optional[str]
    city: Optional[str]
    pincode: str

    # Validator to allow string version of enum value too
    _validate_address_type = validator('address_type',
                                       allow_reuse=True,
                                       pre=True)(allow_string_rep_of_enum)


class AddressListSchema(BaseModel):
    user_id: Optional[int]
    address_type: Optional[AddressType]

    # Validator to allow string version of enum value too
    _validate_address_type = validator('address_type',
                                       allow_reuse=True,
                                       pre=True)(allow_string_rep_of_enum)


# Wishlist Schemas
class WishlistCreateSchema(BaseModel):
    user_id: int
    name: str


class WishlistUpdateSchema(BaseModel):
    user_id: int
    name: str


class WishlistListSchema(BaseModel):
    user_id: Optional[int]
    name: Optional[str]


# WishlistItem Schemas
class WishlistItemCreateSchema(BaseModel):
    wishlist_id: int
    product_variant_id: int


class WishlistItemUpdateSchema(BaseModel):
    wishlist_id: int
    product_variant_id: int


class WishlistItemListSchema(BaseModel):
    wishlist_id: Optional[int]
    product_variant_id: Optional[int]


# Review Schemas
class ReviewCreateSchema(BaseModel):
    user_id: int
    product_id: int
    rating: int
    comment: Optional[str]


class ReviewUpdateSchema(BaseModel):
    user_id: int
    product_id: int
    rating: int
    comment: Optional[str]


class ReviewListSchema(BaseModel):
    user_id: Optional[int]
    product_id: Optional[int]
    rating: Optional[int]


# CartItem Schemas
class CartItemCreateSchema(BaseModel):
    user_id: int
    product_variant_id: int
    quantity: int
    price: condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))


class CartItemUpdateSchema(BaseModel):
    user_id: int
    product_variant_id: int
    quantity: int
    price: condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))


class CartItemListSchema(BaseModel):
    user_id: Optional[int]
    product_variant_id: Optional[int]
