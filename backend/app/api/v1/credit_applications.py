from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

from app.database import get_db
from app.services.credit_service import CreditService
from app.schemas.credit import CreditApplicationCreate, CreditApplicationUpdate, CreditApplicationResponse
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user, require_permission

router = APIRouter()


@router.get("/")
async def list_applications(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    customer_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    credit_service = CreditService(db)
    applications, total = await credit_service.get_applications(
        page=page,
        page_size=page_size,
        search=search,
        status=status,
        customer_id=customer_id
    )
    return PaginatedResponse(
        items=applications,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


@router.get("/{application_id}", response_model=CreditApplicationResponse)
async def get_application(
    application_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    credit_service = CreditService(db)
    application = await credit_service.get_application(application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.post("/", response_model=CreditApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application(
    application_data: CreditApplicationCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:create"))
):
    credit_service = CreditService(db)
    application = await credit_service.create_application(application_data, current_user.id)
    return application


@router.put("/{application_id}", response_model=CreditApplicationResponse)
async def update_application(
    application_id: UUID,
    application_data: CreditApplicationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:update"))
):
    credit_service = CreditService(db)
    application = await credit_service.update_application(application_id, application_data)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.delete("/{application_id}")
async def delete_application(
    application_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:delete"))
):
    credit_service = CreditService(db)
    success = await credit_service.delete_application(application_id)
    if not success:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"message": "Application deleted successfully"}


@router.post("/{application_id}/submit")
async def submit_application(
    application_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:update"))
):
    credit_service = CreditService(db)
    application = await credit_service.submit_application(application_id, current_user.id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.post("/{application_id}/approve")
async def approve_application(
    application_id: UUID,
    notes: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:approve"))
):
    credit_service = CreditService(db)
    application = await credit_service.approve_application(application_id, current_user.id, notes)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.post("/{application_id}/reject")
async def reject_application(
    application_id: UUID,
    reason: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:approve"))
):
    credit_service = CreditService(db)
    application = await credit_service.reject_application(application_id, current_user.id, reason)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application
