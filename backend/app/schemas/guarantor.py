from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class GuarantorBase(BaseModel):
    name: str
    name_ar: Optional[str] = None
    relationship: Optional[str] = None
    type: str
    is_individual: bool = True
    national_id: Optional[str] = None
    commercial_register: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    status: str = "pending"


class GuarantorCreate(GuarantorBase):
    customer_id: UUID


class GuarantorUpdate(BaseModel):
    name: Optional[str] = None
    name_ar: Optional[str] = None
    relationship: Optional[str] = None
    type: Optional[str] = None
    is_individual: Optional[bool] = None
    national_id: Optional[str] = None
    commercial_register: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    status: Optional[str] = None


class GuarantorResponse(GuarantorBase):
    id: UUID
    customer_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class GuarantorFinancialBase(BaseModel):
    assets: dict = {}
    liabilities: dict = {}
    income: dict = {}
    net_worth: Optional[Decimal] = None
    assessment_date: datetime


class GuarantorFinancialCreate(GuarantorFinancialBase):
    guarantor_id: UUID
    assessed_by: Optional[UUID] = None


class GuarantorFinancialResponse(GuarantorFinancialBase):
    id: UUID
    guarantor_id: UUID
    assessed_by: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class GuarantorSupportBase(BaseModel):
    guarantee_type: str
    amount: Decimal
    currency_id: Optional[UUID] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: str = "active"


class GuarantorSupportCreate(GuarantorSupportBase):
    guarantor_id: UUID
    credit_application_id: Optional[UUID] = None


class GuarantorSupportResponse(GuarantorSupportBase):
    id: UUID
    guarantor_id: UUID
    credit_application_id: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
