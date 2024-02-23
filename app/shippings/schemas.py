from _decimal import Decimal
from pydantic.v1 import BaseModel, validator, condecimal
from typing import Optional
from datetime import datetime

from app.shippings.enums import ShipmentStatus, DeliveryStatusStatus
from app.utils.helpers import allow_string_rep_of_enum


# ShippingProvider Schemas
class ShippingProviderCreateSchema(BaseModel):
    name: str
    tracking_url_template: Optional[str] = None
    api_endpoint: Optional[str] = None
    api_key: Optional[str] = None


class ShippingProviderUpdateSchema(BaseModel):
    name: str
    tracking_url_template: Optional[str] = None
    api_endpoint: Optional[str] = None
    api_key: Optional[str] = None


class ShippingProviderListSchema(BaseModel):
    name: Optional[str] = None


# Shipment Schemas
class ShipmentCreateSchema(BaseModel):
    order_id: int
    provider_id: Optional[int] = None
    tracking_number: Optional[str] = None
    shipped_date: Optional[datetime] = None
    estimated_delivery_date: Optional[datetime] = None
    actual_delivery_date: Optional[datetime] = None
    status: ShipmentStatus = ShipmentStatus.PENDING

    @validator('shipped_date', 'estimated_delivery_date', 'actual_delivery_date', pre=True, allow_reuse=True)
    def validate_date(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"time format is incorrect: {e}")
        return v

    _validate_status = validator('status', allow_reuse=True, pre=True)(allow_string_rep_of_enum)


class ShipmentUpdateSchema(BaseModel):
    order_id: int
    provider_id: Optional[int] = None
    tracking_number: Optional[str] = None
    shipped_date: Optional[datetime] = None
    estimated_delivery_date: Optional[datetime] = None
    actual_delivery_date: Optional[datetime] = None
    status: ShipmentStatus = ShipmentStatus.PENDING

    @validator('shipped_date', 'estimated_delivery_date', 'actual_delivery_date', pre=True, allow_reuse=True)
    def validate_date(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"time format is incorrect: {e}")
        return v

    _validate_status = validator('status', allow_reuse=True, pre=True)(allow_string_rep_of_enum)


class ShipmentListSchema(BaseModel):
    order_id: Optional[int] = None
    provider_id: Optional[int] = None
    status: Optional[ShipmentStatus] = None

    _validate_status = validator('status', allow_reuse=True, pre=True)(allow_string_rep_of_enum)


# DeliveryStatus Schemas
class DeliveryStatusCreateSchema(BaseModel):
    shipment_id: int
    status: DeliveryStatusStatus = DeliveryStatusStatus.IN_TRANSIT
    status_date: Optional[datetime] = None
    location: Optional[str] = None
    notes: Optional[str] = None

    @validator('status_date', pre=True, allow_reuse=True)
    def validate_date(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"time format is incorrect: {e}")
        return v

    _validate_status = validator('status', allow_reuse=True, pre=True)(allow_string_rep_of_enum)


class DeliveryStatusUpdateSchema(BaseModel):
    shipment_id: int
    status: DeliveryStatusStatus = DeliveryStatusStatus.IN_TRANSIT
    status_date: Optional[datetime] = None
    location: Optional[str] = None
    notes: Optional[str] = None

    @validator('status_date', pre=True, allow_reuse=True)
    def validate_date(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"time format is incorrect: {e}")
        return v

    _validate_status = validator('status', allow_reuse=True, pre=True)(allow_string_rep_of_enum)


class DeliveryStatusListSchema(BaseModel):
    shipment_id: Optional[int] = None
    status: Optional[DeliveryStatusStatus] = None

    _validate_status = validator('status', allow_reuse=True, pre=True)(allow_string_rep_of_enum)
