from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel
from uuid import UUID

T = TypeVar("T")


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int


class MessageResponse(BaseModel):
    message: str
    success: bool = True
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    errors: Optional[List[dict]] = None


class IDResponse(BaseModel):
    id: UUID


class BulkDeleteRequest(BaseModel):
    ids: List[UUID]


class BulkUpdateRequest(BaseModel):
    ids: List[UUID]
    data: dict
