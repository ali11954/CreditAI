from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class ExposureBase(BaseModel):
    exposure_type: str
    amount: Decimal
    currency_id: Optional[UUID] = None
    details: dict = {}


class ExposureCreate(ExposureBase):
    customer_id: UUID


class ExposureUpdate(BaseModel):
    exposure_type: Optional[str] = None
    amount: Optional[Decimal] = None
    currency_id: Optional[UUID] = None
    details: Optional[dict] = None


class ExposureResponse(ExposureBase):
    id: UUID
    customer_id: UUID
    calculated_at: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ConcentrationLimitBase(BaseModel):
    concentration_type: str
    category: str
    limit_amount: Decimal
    utilized_amount: Decimal = Decimal("0")
    currency_id: Optional[UUID] = None
    threshold_percentage: Optional[Decimal] = None


class ConcentrationLimitCreate(ConcentrationLimitBase):
    pass


class ConcentrationLimitUpdate(BaseModel):
    concentration_type: Optional[str] = None
    category: Optional[str] = None
    limit_amount: Optional[Decimal] = None
    utilized_amount: Optional[Decimal] = None
    currency_id: Optional[UUID] = None
    threshold_percentage: Optional[Decimal] = None


class ConcentrationLimitResponse(ConcentrationLimitBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class StressTestBase(BaseModel):
    name: str
    description: Optional[str] = None
    scenario: dict = {}
    results: dict = {}


class StressTestCreate(StressTestBase):
    conducted_by: Optional[UUID] = None


class StressTestUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    scenario: Optional[dict] = None
    results: Optional[dict] = None


class StressTestResponse(StressTestBase):
    id: UUID
    conducted_at: datetime
    conducted_by: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
