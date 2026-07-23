from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class LegalCaseBase(BaseModel):
    case_number: str
    case_type: str
    court_name: Optional[str] = None
    filing_date: datetime
    status: str = "open"
    amount_in_dispute: Optional[Decimal] = None
    currency_id: Optional[UUID] = None
    assigned_lawyer_id: Optional[UUID] = None
    next_hearing_date: Optional[datetime] = None
    notes: Optional[str] = None


class LegalCaseCreate(LegalCaseBase):
    customer_id: UUID


class LegalCaseUpdate(BaseModel):
    case_number: Optional[str] = None
    case_type: Optional[str] = None
    court_name: Optional[str] = None
    filing_date: Optional[datetime] = None
    status: Optional[str] = None
    amount_in_dispute: Optional[Decimal] = None
    currency_id: Optional[UUID] = None
    assigned_lawyer_id: Optional[UUID] = None
    next_hearing_date: Optional[datetime] = None
    notes: Optional[str] = None


class LegalCaseResponse(LegalCaseBase):
    id: UUID
    customer_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None
    
    class Config:
        from_attributes = True


class LawyerBase(BaseModel):
    name: str
    firm_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    specialization: Optional[str] = None
    license_number: Optional[str] = None


class LawyerCreate(LawyerBase):
    pass


class LawyerUpdate(BaseModel):
    name: Optional[str] = None
    firm_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    specialization: Optional[str] = None
    license_number: Optional[str] = None


class LawyerResponse(LawyerBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CourtHearingBase(BaseModel):
    hearing_date: datetime
    hearing_time: Optional[datetime] = None
    judge: Optional[str] = None
    outcome: Optional[str] = None
    next_date: Optional[datetime] = None
    notes: Optional[str] = None


class CourtHearingCreate(CourtHearingBase):
    case_id: UUID


class CourtHearingUpdate(BaseModel):
    hearing_date: Optional[datetime] = None
    hearing_time: Optional[datetime] = None
    judge: Optional[str] = None
    outcome: Optional[str] = None
    next_date: Optional[datetime] = None
    notes: Optional[str] = None


class CourtHearingResponse(CourtHearingBase):
    id: UUID
    case_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class LegalDocumentBase(BaseModel):
    document_type: str
    title: str
    file_path: Optional[str] = None


class LegalDocumentCreate(LegalDocumentBase):
    case_id: UUID
    uploaded_by: Optional[UUID] = None


class LegalDocumentUpdate(BaseModel):
    document_type: Optional[str] = None
    title: Optional[str] = None
    file_path: Optional[str] = None


class LegalDocumentResponse(LegalDocumentBase):
    id: UUID
    case_id: UUID
    uploaded_by: Optional[UUID] = None
    uploaded_at: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class LegalJudgmentBase(BaseModel):
    judgment_date: datetime
    judgment_type: str
    amount: Optional[Decimal] = None
    description: Optional[str] = None
    appeal_deadline: Optional[datetime] = None


class LegalJudgmentCreate(LegalJudgmentBase):
    case_id: UUID


class LegalJudgmentUpdate(BaseModel):
    judgment_date: Optional[datetime] = None
    judgment_type: Optional[str] = None
    amount: Optional[Decimal] = None
    description: Optional[str] = None
    appeal_deadline: Optional[datetime] = None


class LegalJudgmentResponse(LegalJudgmentBase):
    id: UUID
    case_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class LegalExecutionBase(BaseModel):
    execution_type: str
    status: str = "pending"
    amount: Optional[Decimal] = None
    executed_date: Optional[datetime] = None
    notes: Optional[str] = None


class LegalExecutionCreate(LegalExecutionBase):
    case_id: UUID


class LegalExecutionUpdate(BaseModel):
    execution_type: Optional[str] = None
    status: Optional[str] = None
    amount: Optional[Decimal] = None
    executed_date: Optional[datetime] = None
    notes: Optional[str] = None


class LegalExecutionResponse(LegalExecutionBase):
    id: UUID
    case_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class LegalTimelineBase(BaseModel):
    event_date: datetime
    event_type: str
    description: Optional[str] = None


class LegalTimelineCreate(LegalTimelineBase):
    case_id: UUID
    created_by: Optional[UUID] = None


class LegalTimelineUpdate(BaseModel):
    event_date: Optional[datetime] = None
    event_type: Optional[str] = None
    description: Optional[str] = None


class LegalTimelineResponse(LegalTimelineBase):
    id: UUID
    case_id: UUID
    created_by: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
