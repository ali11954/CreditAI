from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

from app.database import get_db
from app.services.credit_service import CreditService
from app.schemas.credit import CreditLimitCreate, CreditLimitUpdate, CreditLimitResponse
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user, require_permission

router = APIRouter()


@router.get("/")
async def list_credit_limits(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    customer_id: Optional[UUID] = None,
    limit_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    credit_service = CreditService(db)
    limits, total = await credit_service.get_credit_limits(
        page=page,
        page_size=page_size,
        customer_id=customer_id,
        limit_type=limit_type
    )
    return PaginatedResponse(
        items=limits,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


@router.get("/{limit_id}", response_model=CreditLimitResponse)
async def get_credit_limit(
    limit_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    credit_service = CreditService(db)
    limit = await credit_service.get_credit_limit(limit_id)
    if not limit:
        raise HTTPException(status_code=404, detail="Credit limit not found")
    return limit


@router.post("/", response_model=CreditLimitResponse, status_code=status.HTTP_201_CREATED)
async def create_credit_limit(
    limit_data: CreditLimitCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:create"))
):
    credit_service = CreditService(db)
    limit = await credit_service.create_credit_limit(limit_data, current_user.id)
    return limit


@router.put("/{limit_id}", response_model=CreditLimitResponse)
async def update_credit_limit(
    limit_id: UUID,
    limit_data: CreditLimitUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:update"))
):
    credit_service = CreditService(db)
    limit = await credit_service.update_credit_limit(limit_id, limit_data)
    if not limit:
        raise HTTPException(status_code=404, detail="Credit limit not found")
    return limit


@router.delete("/{limit_id}")
async def delete_credit_limit(
    limit_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:delete"))
):
    credit_service = CreditService(db)
    success = await credit_service.delete_credit_limit(limit_id)
    if not success:
        raise HTTPException(status_code=404, detail="Credit limit not found")
    return {"message": "Credit limit deleted successfully"}


@router.get("/{limit_id}/history")
async def get_limit_history(
    limit_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    credit_service = CreditService(db)
    history = await credit_service.get_limit_history(limit_id)
    return {"items": history}
