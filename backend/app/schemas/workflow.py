from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class WorkflowTemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    module: str
    is_active: bool = True
    steps: List[dict] = []


class WorkflowTemplateCreate(WorkflowTemplateBase):
    pass


class WorkflowTemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    module: Optional[str] = None
    is_active: Optional[bool] = None
    steps: Optional[List[dict]] = None


class WorkflowTemplateResponse(WorkflowTemplateBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class WorkflowInstanceBase(BaseModel):
    entity_type: str
    entity_id: UUID
    status: str = "in_progress"
    current_step: int = 1


class WorkflowInstanceCreate(WorkflowInstanceBase):
    template_id: UUID
    initiated_by: UUID


class WorkflowInstanceUpdate(BaseModel):
    status: Optional[str] = None
    current_step: Optional[int] = None
    completed_at: Optional[datetime] = None


class WorkflowInstanceResponse(WorkflowInstanceBase):
    id: UUID
    template_id: UUID
    initiated_by: UUID
    initiated_at: datetime
    completed_at: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class WorkflowStepBase(BaseModel):
    step_number: int
    name: str
    status: str = "pending"
    action: Optional[str] = None
    comments: Optional[str] = None


class WorkflowStepCreate(WorkflowStepBase):
    instance_id: UUID
    assignee_id: Optional[UUID] = None


class WorkflowStepUpdate(BaseModel):
    step_number: Optional[int] = None
    name: Optional[str] = None
    assignee_id: Optional[UUID] = None
    status: Optional[str] = None
    action: Optional[str] = None
    comments: Optional[str] = None
    completed_at: Optional[datetime] = None


class WorkflowStepResponse(WorkflowStepBase):
    id: UUID
    instance_id: UUID
    assignee_id: Optional[UUID] = None
    completed_at: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ApprovalMatrixBase(BaseModel):
    module: str
    action: str
    conditions: dict = {}
    approvers: List[dict] = []
    is_active: bool = True


class ApprovalMatrixCreate(ApprovalMatrixBase):
    pass


class ApprovalMatrixUpdate(BaseModel):
    module: Optional[str] = None
    action: Optional[str] = None
    conditions: Optional[dict] = None
    approvers: Optional[List[dict]] = None
    is_active: Optional[bool] = None


class ApprovalMatrixResponse(ApprovalMatrixBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
