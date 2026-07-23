from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

from app.database import get_db
from app.services.credit_service import CreditService
from app.schemas.credit import CreditAnalysisCreate, CreditAnalysisUpdate, CreditAnalysisResponse
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user, require_permission

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[CreditAnalysisResponse])
async def list_analyses(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    application_id: Optional[UUID] = None,
    customer_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    credit_service = CreditService(db)
    analyses, total = await credit_service.get_analyses(
        page=page,
        page_size=page_size,
        application_id=application_id,
        customer_id=customer_id
    )
    return PaginatedResponse(
        items=analyses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


@router.get("/{analysis_id}", response_model=CreditAnalysisResponse)
async def get_analysis(
    analysis_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    credit_service = CreditService(db)
    analysis = await credit_service.get_analysis(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis


@router.post("/", response_model=CreditAnalysisResponse, status_code=status.HTTP_201_CREATED)
async def create_analysis(
    analysis_data: CreditAnalysisCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:create"))
):
    credit_service = CreditService(db)
    analysis = await credit_service.create_analysis(analysis_data, current_user.id)
    return analysis


@router.put("/{analysis_id}", response_model=CreditAnalysisResponse)
async def update_analysis(
    analysis_id: UUID,
    analysis_data: CreditAnalysisUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:update"))
):
    credit_service = CreditService(db)
    analysis = await credit_service.update_analysis(analysis_id, analysis_data)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis


@router.delete("/{analysis_id}")
async def delete_analysis(
    analysis_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:delete"))
):
    credit_service = CreditService(db)
    success = await credit_service.delete_analysis(analysis_id)
    if not success:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return {"message": "Analysis deleted successfully"}
