from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class ReportTemplateBase(BaseModel):
    name: str
    name_ar: Optional[str] = None
    title_en: Optional[str] = None
    description: Optional[str] = None
    module: str
    query_template: str
    parameters: Optional[dict] = None
    format: str = "pdf"
    icon: Optional[str] = None
    color: Optional[str] = None
    is_active: bool = True


class ReportTemplateCreate(ReportTemplateBase):
    company_id: Optional[UUID] = None


class ReportTemplateUpdate(BaseModel):
    name: Optional[str] = None
    name_ar: Optional[str] = None
    description: Optional[str] = None
    module: Optional[str] = None
    query_template: Optional[str] = None
    parameters: Optional[dict] = None
    format: Optional[str] = None
    is_active: Optional[bool] = None


class ReportTemplateResponse(ReportTemplateBase):
    id: UUID
    company_id: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ReportExecutionBase(BaseModel):
    parameters: dict = {}
    status: str = "pending"
    file_path: Optional[str] = None
    executed_at: Optional[datetime] = None


class ReportExecutionCreate(ReportExecutionBase):
    template_id: UUID
    executed_by: Optional[UUID] = None


class ReportExecutionUpdate(BaseModel):
    status: Optional[str] = None
    file_path: Optional[str] = None
    completed_at: Optional[datetime] = None


class ReportExecutionResponse(ReportExecutionBase):
    id: UUID
    template_id: UUID
    executed_by: Optional[UUID] = None
    completed_at: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DashboardBase(BaseModel):
    name: str
    name_ar: Optional[str] = None
    layout: dict = {}
    widgets: List[dict] = []
    is_default: bool = False


class DashboardCreate(DashboardBase):
    company_id: Optional[UUID] = None
    created_by: Optional[UUID] = None


class DashboardUpdate(BaseModel):
    name: Optional[str] = None
    name_ar: Optional[str] = None
    layout: Optional[dict] = None
    widgets: Optional[List[dict]] = None
    is_default: Optional[bool] = None


class DashboardResponse(DashboardBase):
    id: UUID
    company_id: Optional[UUID] = None
    created_by: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DashboardWidgetBase(BaseModel):
    name: str
    type: str
    config: dict = {}
    data_source: Optional[str] = None
    position: dict = {"x": 0, "y": 0}
    size: dict = {"w": 6, "h": 4}


class DashboardWidgetCreate(DashboardWidgetBase):
    dashboard_id: UUID


class DashboardWidgetUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    config: Optional[dict] = None
    data_source: Optional[str] = None
    position: Optional[dict] = None
    size: Optional[dict] = None


class DashboardWidgetResponse(DashboardWidgetBase):
    id: UUID
    dashboard_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
