from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class CollateralBase(BaseModel):
    type: str
    description: Optional[str] = None
    estimated_value: Optional[Decimal] = None
    assessed_value: Optional[Decimal] = None
    currency_id: Optional[UUID] = None
    status: str = "active"
    registration_number: Optional[str] = None
    location: Optional[str] = None
    expiry_date: Optional[datetime] = None
    insurance_required: bool = False
    notes: Optional[str] = None
    images: List[str] = []


class CollateralCreate(CollateralBase):
    customer_id: UUID


class CollateralUpdate(BaseModel):
    type: Optional[str] = None
    description: Optional[str] = None
    estimated_value: Optional[Decimal] = None
    assessed_value: Optional[Decimal] = None
    currency_id: Optional[UUID] = None
    status: Optional[str] = None
    registration_number: Optional[str] = None
    location: Optional[str] = None
    expiry_date: Optional[datetime] = None
    insurance_required: Optional[bool] = None
    notes: Optional[str] = None
    images: Optional[List[str]] = None


class CollateralResponse(CollateralBase):
    id: UUID
    customer_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CollateralValuationBase(BaseModel):
    valuation_date: datetime
    value: Decimal
    methodology: Optional[str] = None
    valuator: Optional[str] = None
    next_valuation_date: Optional[datetime] = None


class CollateralValuationCreate(CollateralValuationBase):
    collateral_id: UUID


class CollateralValuationResponse(CollateralValuationBase):
    id: UUID
    collateral_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CollateralReleaseBase(BaseModel):
    released_at: datetime
    reason: Optional[str] = None


class CollateralReleaseCreate(CollateralReleaseBase):
    collateral_id: UUID
    released_by: UUID
    approved_by: Optional[UUID] = None


class CollateralReleaseResponse(CollateralReleaseBase):
    id: UUID
    collateral_id: UUID
    released_by: UUID
    approved_by: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
