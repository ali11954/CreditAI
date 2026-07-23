from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class CommunicationTemplateBase(BaseModel):
    name: str
    name_ar: Optional[str] = None
    type: str
    subject: Optional[str] = None
    body: str
    variables: List[str] = []
    is_active: bool = True


class CommunicationTemplateCreate(CommunicationTemplateBase):
    company_id: Optional[UUID] = None


class CommunicationTemplateUpdate(BaseModel):
    name: Optional[str] = None
    name_ar: Optional[str] = None
    type: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    variables: Optional[List[str]] = None
    is_active: Optional[bool] = None


class CommunicationTemplateResponse(CommunicationTemplateBase):
    id: UUID
    company_id: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CommunicationLogBase(BaseModel):
    type: str
    direction: str = "outbound"
    recipient: Optional[str] = None
    subject: Optional[str] = None
    content: Optional[str] = None
    status: str = "sent"
    sent_at: datetime


class CommunicationLogCreate(CommunicationLogBase):
    customer_id: Optional[UUID] = None
    created_by: Optional[UUID] = None


class CommunicationLogUpdate(BaseModel):
    type: Optional[str] = None
    direction: Optional[str] = None
    recipient: Optional[str] = None
    subject: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None


class CommunicationLogResponse(CommunicationLogBase):
    id: UUID
    customer_id: Optional[UUID] = None
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    created_by: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CampaignBase(BaseModel):
    name: str
    type: str
    target_audience: dict = {}
    template_id: Optional[UUID] = None
    scheduled_date: Optional[datetime] = None
    status: str = "draft"
    sent_count: int = 0
    opened_count: int = 0


class CampaignCreate(CampaignBase):
    company_id: Optional[UUID] = None


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    target_audience: Optional[dict] = None
    template_id: Optional[UUID] = None
    scheduled_date: Optional[datetime] = None
    status: Optional[str] = None


class CampaignResponse(CampaignBase):
    id: UUID
    company_id: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
