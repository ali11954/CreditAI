from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class SystemSettingBase(BaseModel):
    key: str
    value: Optional[str] = None
    value_type: str = "string"
    description: Optional[str] = None
    module: Optional[str] = None


class SystemSettingCreate(SystemSettingBase):
    pass


class SystemSettingUpdate(BaseModel):
    value: Optional[str] = None
    value_type: Optional[str] = None
    description: Optional[str] = None
    module: Optional[str] = None
    is_active: Optional[bool] = None


class SystemSettingResponse(SystemSettingBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ModuleConfigBase(BaseModel):
    module_name: str
    is_enabled: bool = True
    settings: dict = {}


class ModuleConfigCreate(ModuleConfigBase):
    company_id: Optional[UUID] = None


class ModuleConfigUpdate(BaseModel):
    module_name: Optional[str] = None
    is_enabled: Optional[bool] = None
    settings: Optional[dict] = None


class ModuleConfigResponse(ModuleConfigBase):
    id: UUID
    company_id: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MenuConfigBase(BaseModel):
    name: str
    name_ar: Optional[str] = None
    icon: Optional[str] = None
    url: Optional[str] = None
    parent_id: Optional[UUID] = None
    sort_order: str = "0"
    is_visible: bool = True
    permission_required: Optional[str] = None
    module: Optional[str] = None


class MenuConfigCreate(MenuConfigBase):
    pass


class MenuConfigUpdate(BaseModel):
    name: Optional[str] = None
    name_ar: Optional[str] = None
    icon: Optional[str] = None
    url: Optional[str] = None
    parent_id: Optional[UUID] = None
    sort_order: Optional[str] = None
    is_visible: Optional[bool] = None
    permission_required: Optional[str] = None
    module: Optional[str] = None
    is_active: Optional[bool] = None


class MenuConfigResponse(MenuConfigBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
