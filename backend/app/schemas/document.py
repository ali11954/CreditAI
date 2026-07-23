from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class DocumentFolderBase(BaseModel):
    name: str
    parent_id: Optional[UUID] = None
    is_shared: bool = False


class DocumentFolderCreate(DocumentFolderBase):
    company_id: Optional[UUID] = None
    created_by: Optional[UUID] = None


class DocumentFolderUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[UUID] = None
    is_shared: Optional[bool] = None


class DocumentFolderResponse(DocumentFolderBase):
    id: UUID
    company_id: Optional[UUID] = None
    created_by: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DocumentBase(BaseModel):
    name: str
    file_path: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    version: int = 1
    description: Optional[str] = None
    tags: List[str] = []
    extra_data: Optional[dict] = None


class DocumentCreate(DocumentBase):
    folder_id: Optional[UUID] = None
    uploaded_by: Optional[UUID] = None


class DocumentUpdate(BaseModel):
    name: Optional[str] = None
    folder_id: Optional[UUID] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    extra_data: Optional[dict] = None


class DocumentResponse(DocumentBase):
    id: UUID
    folder_id: Optional[UUID] = None
    uploaded_by: Optional[UUID] = None
    uploaded_at: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DocumentVersionBase(BaseModel):
    version: int
    file_path: str
    notes: Optional[str] = None


class DocumentVersionCreate(DocumentVersionBase):
    document_id: UUID
    uploaded_by: Optional[UUID] = None


class DocumentVersionResponse(DocumentVersionBase):
    id: UUID
    document_id: UUID
    uploaded_by: Optional[UUID] = None
    uploaded_at: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DocumentOCRBase(BaseModel):
    extracted_text: Optional[str] = None
    confidence: Optional[int] = None
    language: Optional[str] = None


class DocumentOCRCreate(DocumentOCRBase):
    document_id: UUID


class DocumentOCRResponse(DocumentOCRBase):
    id: UUID
    document_id: UUID
    processed_at: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DocumentApprovalBase(BaseModel):
    status: str = "pending"
    comments: Optional[str] = None
    approved_at: Optional[datetime] = None


class DocumentApprovalCreate(DocumentApprovalBase):
    document_id: UUID
    approver_id: UUID


class DocumentApprovalUpdate(BaseModel):
    status: Optional[str] = None
    comments: Optional[str] = None
    approved_at: Optional[datetime] = None


class DocumentApprovalResponse(DocumentApprovalBase):
    id: UUID
    document_id: UUID
    approver_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
