from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class AuditTrailBase(BaseModel):
    action: str
    entity_type: str
    entity_id: Optional[UUID] = None
    old_values: dict = {}
    new_values: dict = {}
    ip_address: Optional[str] = None
    timestamp: datetime


class AuditTrailCreate(AuditTrailBase):
    user_id: Optional[UUID] = None


class AuditTrailResponse(AuditTrailBase):
    id: UUID
    user_id: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AIDecisionLogBase(BaseModel):
    model_name: str
    input_data: dict = {}
    output_data: dict = {}
    confidence: Optional[int] = None
    execution_time_ms: Optional[int] = None
    entity_type: Optional[str] = None
    entity_id: Optional[UUID] = None
    timestamp: datetime


class AIDecisionLogCreate(AIDecisionLogBase):
    user_id: Optional[UUID] = None


class AIDecisionLogResponse(AIDecisionLogBase):
    id: UUID
    user_id: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SecurityEventBase(BaseModel):
    event_type: str
    ip_address: Optional[str] = None
    details: dict = {}
    severity: str = "info"
    timestamp: datetime


class SecurityEventCreate(SecurityEventBase):
    user_id: Optional[UUID] = None


class SecurityEventResponse(SecurityEventBase):
    id: UUID
    user_id: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
