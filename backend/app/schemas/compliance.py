from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class KYCRecordBase(BaseModel):
    type: str
    status: str = "pending"
    documents: List[dict] = []
    notes: Optional[str] = None


class KYCRecordCreate(KYCRecordBase):
    customer_id: UUID


class KYCRecordUpdate(BaseModel):
    status: Optional[str] = None
    documents: Optional[List[dict]] = None
    notes: Optional[str] = None
    expires_at: Optional[datetime] = None


class KYCRecordResponse(KYCRecordBase):
    id: UUID
    customer_id: UUID
    verified_by: Optional[UUID] = None
    verified_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AMLCheckBase(BaseModel):
    check_type: str
    result: str
    score: Optional[int] = None
    details: dict = {}


class AMLCheckCreate(AMLCheckBase):
    customer_id: UUID


class AMLCheckResponse(AMLCheckBase):
    id: UUID
    customer_id: UUID
    checked_at: datetime
    checked_by: Optional[UUID] = None
    is_active: bool
    
    class Config:
        from_attributes = True


class PEPCheckBase(BaseModel):
    is_pep: bool = False
    pep_type: Optional[str] = None
    details: Optional[str] = None


class PEPCheckCreate(PEPCheckBase):
    customer_id: UUID


class PEPCheckResponse(PEPCheckBase):
    id: UUID
    customer_id: UUID
    checked_at: datetime
    checked_by: Optional[UUID] = None
    is_active: bool
    
    class Config:
        from_attributes = True


class SanctionCheckBase(BaseModel):
    is_sanctioned: bool = False
    list_name: Optional[str] = None
    details: Optional[str] = None


class SanctionCheckCreate(SanctionCheckBase):
    customer_id: UUID


class SanctionCheckResponse(SanctionCheckBase):
    id: UUID
    customer_id: UUID
    checked_at: datetime
    checked_by: Optional[UUID] = None
    is_active: bool
    
    class Config:
        from_attributes = True


class ComplianceCaseBase(BaseModel):
    case_type: str
    status: str = "open"
    priority: str = "medium"
    assigned_to: Optional[UUID] = None
    due_date: Optional[datetime] = None
    resolution: Optional[str] = None
    resolution_date: Optional[datetime] = None
    notes: Optional[str] = None


class ComplianceCaseCreate(ComplianceCaseBase):
    customer_id: UUID


class ComplianceCaseUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[UUID] = None
    due_date: Optional[datetime] = None
    resolution: Optional[str] = None
    resolution_date: Optional[datetime] = None
    notes: Optional[str] = None


class ComplianceCaseResponse(ComplianceCaseBase):
    id: UUID
    customer_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DueDiligenceBase(BaseModel):
    type: str
    status: str = "pending"
    findings: dict = {}
    risk_level: Optional[str] = None


class DueDiligenceCreate(DueDiligenceBase):
    customer_id: UUID
    conducted_by: Optional[UUID] = None


class DueDiligenceUpdate(BaseModel):
    status: Optional[str] = None
    findings: Optional[dict] = None
    risk_level: Optional[str] = None
    conducted_at: Optional[datetime] = None


class DueDiligenceResponse(DueDiligenceBase):
    id: UUID
    customer_id: UUID
    conducted_by: Optional[UUID] = None
    conducted_at: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
