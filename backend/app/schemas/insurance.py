from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class InsuranceCompanyBase(BaseModel):
    name: str
    name_ar: Optional[str] = None
    license_number: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


class InsuranceCompanyCreate(InsuranceCompanyBase):
    pass


class InsuranceCompanyUpdate(BaseModel):
    name: Optional[str] = None
    name_ar: Optional[str] = None
    license_number: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


class InsuranceCompanyResponse(InsuranceCompanyBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class InsurancePolicyBase(BaseModel):
    policy_number: str
    policy_type: str
    coverage_amount: Optional[Decimal] = None
    premium: Optional[Decimal] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: str = "active"
    documents: List[dict] = []


class InsurancePolicyCreate(InsurancePolicyBase):
    customer_id: UUID
    insurance_company_id: UUID


class InsurancePolicyUpdate(BaseModel):
    policy_number: Optional[str] = None
    policy_type: Optional[str] = None
    coverage_amount: Optional[Decimal] = None
    premium: Optional[Decimal] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None
    documents: Optional[List[dict]] = None


class InsurancePolicyResponse(InsurancePolicyBase):
    id: UUID
    customer_id: UUID
    insurance_company_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class InsuranceClaimBase(BaseModel):
    claim_number: str
    claim_date: datetime
    amount: Optional[Decimal] = None
    status: str = "pending"
    description: Optional[str] = None
    resolution: Optional[str] = None
    resolved_date: Optional[datetime] = None


class InsuranceClaimCreate(InsuranceClaimBase):
    policy_id: UUID


class InsuranceClaimUpdate(BaseModel):
    claim_number: Optional[str] = None
    amount: Optional[Decimal] = None
    status: Optional[str] = None
    description: Optional[str] = None
    resolution: Optional[str] = None
    resolved_date: Optional[datetime] = None


class InsuranceClaimResponse(InsuranceClaimBase):
    id: UUID
    policy_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
