from _decimal import Decimal
from pydantic.v1 import BaseModel, validator, condecimal
from typing import Optional
from datetime import datetime

from app.payments.enums import PaymentMethod, PaymentStatus, RefundType, ReturnStatus, RefundStatus
from app.utils.helpers import allow_string_rep_of_enum, convert_to_decimal


# Payment Schemas
class PaymentCreateSchema(BaseModel):
    order_id: int
    amount: condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))
    payment_method: PaymentMethod
    payment_status: PaymentStatus
    transaction_id: Optional[str] = None
    metadata: Optional[dict] = None

    # Validator to allow string version of enum value too
    _validate_payment_method = validator('payment_method',
                                         allow_reuse=True,
                                         pre=True)(allow_string_rep_of_enum)
    # Validator to allow string version of enum value too
    _validate_payment_status = validator('payment_status',
                                         allow_reuse=True,
                                         pre=True)(allow_string_rep_of_enum)


class PaymentUpdateSchema(BaseModel):
    order_id: int
    amount: condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))
    payment_method: PaymentMethod
    payment_status: PaymentStatus
    transaction_id: Optional[str] = None
    metadata: Optional[dict] = None

    # Validator to allow string version of enum value too
    _validate_payment_method = validator('payment_method',
                                         allow_reuse=True,
                                         pre=True)(allow_string_rep_of_enum)
    # Validator to allow string version of enum value too
    _validate_payment_status = validator('payment_status',
                                         allow_reuse=True,
                                         pre=True)(allow_string_rep_of_enum)


class PaymentListSchema(BaseModel):
    order_id: Optional[int]
    payment_method: Optional[PaymentMethod]
    payment_status: Optional[PaymentStatus]
    transaction_id: Optional[str]

    # Validator to allow string version of enum value too
    _validate_payment_method = validator('payment_method',
                                         allow_reuse=True,
                                         pre=True)(allow_string_rep_of_enum)
    # Validator to allow string version of enum value too
    _validate_payment_status = validator('payment_status',
                                         allow_reuse=True,
                                         pre=True)(allow_string_rep_of_enum)


# Return Schemas
class ReturnCreateSchema(BaseModel):
    order_id: int
    reason: str
    status: Optional[ReturnStatus] = ReturnStatus.REQUESTED

    # Validator to allow string version of enum value too
    _validate_return_status = validator('status',
                                        allow_reuse=True,
                                        pre=True)(allow_string_rep_of_enum)


class ReturnUpdateSchema(BaseModel):
    order_id: int
    reason: str
    status: ReturnStatus

    # Validator to allow string version of enum value too
    _validate_return_status = validator('status',
                                        allow_reuse=True,
                                        pre=True)(allow_string_rep_of_enum)


class ReturnListSchema(BaseModel):
    order_id: Optional[int]
    status: Optional[ReturnStatus]

    # Validator to allow string version of enum value too
    _validate_return_status = validator('status',
                                        allow_reuse=True,
                                        pre=True)(allow_string_rep_of_enum)


# Refund Schemas
class RefundCreateSchema(BaseModel):
    return_obj_id: Optional[int]
    payment_id: int
    refund_type: RefundType
    amount: condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))
    reason: Optional[str] = None
    status: Optional[RefundStatus] = RefundStatus.INITIATED
    metadata: Optional[dict] = None

    # Validator to allow string version of enum value too
    _validate_enum = validator('refund_type', 'status',
                               allow_reuse=True,
                               pre=True)(allow_string_rep_of_enum)


class RefundUpdateSchema(BaseModel):
    return_obj_id: Optional[int]
    payment_id: int
    refund_type: RefundType
    amount: condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))
    reason: Optional[str] = None
    status: Optional[RefundStatus] = RefundStatus.INITIATED
    metadata: Optional[dict] = None

    # Validator to allow string version of enum value too
    _validate_enum = validator('refund_type', 'status',
                               allow_reuse=True,
                               pre=True)(allow_string_rep_of_enum)


class RefundListSchema(BaseModel):
    return_obj_id: Optional[int]
    payment_id: Optional[int]
    refund_type: Optional[RefundType]
    status: Optional[RefundStatus]

    # Validator to allow string version of enum value too
    _validate_enum = validator('refund_type', 'status',
                               allow_reuse=True,
                               pre=True)(allow_string_rep_of_enum)


# ReturnItem Schemas
class ReturnItemCreateSchema(BaseModel):
    return_obj_id: int
    product_variant_id: int
    quantity: int


class ReturnItemUpdateSchema(BaseModel):
    return_obj_id: int
    product_variant_id: int
    quantity: int


class ReturnItemListSchema(BaseModel):
    return_obj_id: Optional[int]
    product_variant_id: Optional[int]
