from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class NotificationBase(BaseModel):
    title: str
    title_ar: Optional[str] = None
    message: str
    message_ar: Optional[str] = None
    type: str
    entity_type: Optional[str] = None
    entity_id: Optional[UUID] = None
    is_read: bool = False
    read_at: Optional[datetime] = None
    action_url: Optional[str] = None


class NotificationCreate(NotificationBase):
    user_id: UUID


class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None
    read_at: Optional[datetime] = None


class NotificationResponse(NotificationBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    is_active: bool
    updated_at: datetime
    
    class Config:
        from_attributes = True


class NotificationPreferenceBase(BaseModel):
    notification_type: str
    channel: str
    is_enabled: bool = True


class NotificationPreferenceCreate(NotificationPreferenceBase):
    user_id: UUID


class NotificationPreferenceUpdate(BaseModel):
    notification_type: Optional[str] = None
    channel: Optional[str] = None
    is_enabled: Optional[bool] = None


class NotificationPreferenceResponse(NotificationPreferenceBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
