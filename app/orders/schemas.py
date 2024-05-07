from _decimal import Decimal
from pydantic.v1 import BaseModel, validator, condecimal
from typing import Optional
from datetime import datetime

from app.orders.enums import OrderStatus
from app.utils.helpers import allow_string_rep_of_enum, convert_to_decimal


# Order Schemas
class OrderCreateSchema(BaseModel):
    user_id: int
    coupon_id: Optional[int] = None
    status: Optional[OrderStatus] = OrderStatus.PENDING

    _validate_status = validator('status', allow_reuse=True, pre=True)(allow_string_rep_of_enum)


class OrderUpdateSchema(BaseModel):
    user_id: int = None
    coupon_id: Optional[int] = None
    status: Optional[OrderStatus] = None

    _validate_status = validator('status', allow_reuse=True, pre=True)(allow_string_rep_of_enum)


class OrderListSchema(BaseModel):
    user_id: Optional[int]
    coupon_id: Optional[int]
    status: Optional[OrderStatus]

    _validate_status = validator('status', allow_reuse=True, pre=True)(allow_string_rep_of_enum)


# OrderItem Schemas
class OrderItemCreateSchema(BaseModel):
    order_id: int
    product_variant_id: int
    quantity: int
    price: condecimal(max_digits=10, decimal_places=2)


class OrderItemUpdateSchema(BaseModel):
    order_id: int
    product_variant_id: int
    quantity: int
    price: condecimal(max_digits=10, decimal_places=2)


class OrderItemListSchema(BaseModel):
    order_id: Optional[int] = None
    product_variant_id: Optional[int] = None
