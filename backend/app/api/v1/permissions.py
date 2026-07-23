from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

from app.database import get_db
from app.services.user_service import UserService
from app.schemas.user import PermissionCreate, PermissionResponse
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user, require_permission

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[PermissionResponse])
async def list_permissions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    module: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("permissions:read"))
):
    user_service = UserService(db)
    permissions, total = await user_service.get_permissions(
        page=page,
        page_size=page_size,
        module=module
    )
    return PaginatedResponse(
        items=permissions,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


@router.get("/{permission_id}", response_model=PermissionResponse)
async def get_permission(
    permission_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("permissions:read"))
):
    user_service = UserService(db)
    permission = await user_service.get_permission(permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission


@router.post("/", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
async def create_permission(
    permission_data: PermissionCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("permissions:create"))
):
    user_service = UserService(db)
    permission = await user_service.create_permission(permission_data)
    return permission


@router.delete("/{permission_id}")
async def delete_permission(
    permission_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("permissions:delete"))
):
    user_service = UserService(db)
    success = await user_service.delete_permission(permission_id)
    if not success:
        raise HTTPException(status_code=404, detail="Permission not found")
    return {"message": "Permission deleted successfully"}
