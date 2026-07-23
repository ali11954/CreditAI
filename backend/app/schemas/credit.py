from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class CreditApplicationBase(BaseModel):
    application_type: str
    requested_amount: Decimal
    currency_id: Optional[UUID] = None
    purpose: Optional[str] = None


class CreditApplicationCreate(CreditApplicationBase):
    customer_id: UUID
    submitted_by: Optional[UUID] = None


class CreditApplicationUpdate(BaseModel):
    application_type: Optional[str] = None
    requested_amount: Optional[Decimal] = None
    currency_id: Optional[UUID] = None
    purpose: Optional[str] = None
    status: Optional[str] = None
    rejection_reason: Optional[str] = None
    conditions: Optional[List[dict]] = None
    notes: Optional[str] = None


class CreditApplicationResponse(CreditApplicationBase):
    id: UUID
    customer_id: UUID
    customer_name: Optional[str] = None
    currency_code: Optional[str] = None
    status: str
    submitted_by: Optional[UUID] = None
    submitted_at: Optional[datetime] = None
    reviewed_by: Optional[UUID] = None
    reviewed_at: Optional[datetime] = None
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    conditions: List[dict] = []
    notes: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CreditAnalysisBase(BaseModel):
    analysis_type: str
    financial_data: dict = {}
    ratios: dict = {}
    cash_flow: dict = {}
    risk_rating: Optional[str] = None
    credit_score: Optional[int] = None
    ai_recommendation: Optional[str] = None
    analyst_notes: Optional[str] = None


class CreditAnalysisCreate(CreditAnalysisBase):
    application_id: UUID
    customer_id: UUID
    analyst_id: Optional[UUID] = None


class CreditAnalysisUpdate(BaseModel):
    analysis_type: Optional[str] = None
    financial_data: Optional[dict] = None
    ratios: Optional[dict] = None
    cash_flow: Optional[dict] = None
    risk_rating: Optional[str] = None
    credit_score: Optional[int] = None
    ai_recommendation: Optional[str] = None
    analyst_notes: Optional[str] = None


class CreditAnalysisResponse(CreditAnalysisBase):
    id: UUID
    application_id: UUID
    customer_id: UUID
    analyst_id: Optional[UUID] = None
    analyzed_at: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CreditCommitteeBase(BaseModel):
    name: str
    description: Optional[str] = None
    meeting_date: Optional[datetime] = None
    status: str = "active"


class CreditCommitteeCreate(CreditCommitteeBase):
    company_id: UUID


class CreditCommitteeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    meeting_date: Optional[datetime] = None
    status: Optional[str] = None
    minutes: Optional[str] = None


class CreditCommitteeResponse(CreditCommitteeBase):
    id: UUID
    company_id: UUID
    minutes: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CommitteeMemberBase(BaseModel):
    user_id: UUID
    role_in_committee: str = "member"


class CommitteeMemberCreate(CommitteeMemberBase):
    committee_id: UUID


class CommitteeMemberResponse(CommitteeMemberBase):
    committee_id: UUID
    is_active: bool
    assigned_at: datetime
    
    class Config:
        from_attributes = True


class CommitteeDecisionBase(BaseModel):
    decision: str
    conditions: List[dict] = []
    vote: str
    comments: Optional[str] = None


class CommitteeDecisionCreate(CommitteeDecisionBase):
    committee_id: UUID
    application_id: UUID
    voted_by: UUID


class CommitteeDecisionUpdate(BaseModel):
    decision: Optional[str] = None
    conditions: Optional[List[dict]] = None
    vote: Optional[str] = None
    comments: Optional[str] = None


class CommitteeDecisionResponse(CommitteeDecisionBase):
    id: UUID
    committee_id: UUID
    application_id: UUID
    voted_by: UUID
    vote_date: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CreditLimitBase(BaseModel):
    limit_type: str
    amount: Decimal
    currency_id: Optional[UUID] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class CreditLimitCreate(CreditLimitBase):
    customer_id: UUID
    parent_limit_id: Optional[UUID] = None


class CreditLimitUpdate(BaseModel):
    limit_type: Optional[str] = None
    amount: Optional[Decimal] = None
    currency_id: Optional[UUID] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None


class CreditLimitResponse(CreditLimitBase):
    id: UUID
    customer_id: UUID
    customer_name: Optional[str] = None
    currency_code: Optional[str] = None
    utilized_amount: Decimal
    available_amount: Decimal
    reserved_amount: Decimal
    status: str
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None
    parent_limit_id: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CreditLimitHistoryBase(BaseModel):
    action: str
    old_amount: Optional[Decimal] = None
    new_amount: Optional[Decimal] = None
    reason: Optional[str] = None


class CreditLimitHistoryCreate(CreditLimitHistoryBase):
    limit_id: UUID
    changed_by: UUID


class CreditLimitHistoryResponse(CreditLimitHistoryBase):
    id: UUID
    limit_id: UUID
    changed_by: UUID
    changed_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


class CreditScoreBase(BaseModel):
    score: int
    factors: dict = {}
    methodology: Optional[str] = None
    version: Optional[str] = None


class CreditScoreCreate(CreditScoreBase):
    customer_id: UUID


class CreditScoreResponse(CreditScoreBase):
    id: UUID
    customer_id: UUID
    calculated_at: datetime
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
