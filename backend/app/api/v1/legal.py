from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

from app.database import get_db
from app.services.legal_service import LegalService
from app.schemas.legal import LegalCaseCreate, LegalCaseUpdate, LegalCaseResponse
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user, require_permission

router = APIRouter()


@router.get("/cases", response_model=PaginatedResponse[LegalCaseResponse])
async def list_cases(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    customer_id: Optional[UUID] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("legal:read"))
):
    legal_service = LegalService(db)
    cases, total = await legal_service.get_cases(
        page=page,
        page_size=page_size,
        customer_id=customer_id,
        status=status
    )
    return PaginatedResponse(
        items=cases,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


@router.get("/cases/{case_id}", response_model=LegalCaseResponse)
async def get_case(
    case_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("legal:read"))
):
    legal_service = LegalService(db)
    case = await legal_service.get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Legal case not found")
    return case


@router.post("/cases", response_model=LegalCaseResponse, status_code=status.HTTP_201_CREATED)
async def create_case(
    case_data: LegalCaseCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("legal:create"))
):
    legal_service = LegalService(db)
    case = await legal_service.create_case(case_data, current_user.id)
    return case


@router.put("/cases/{case_id}", response_model=LegalCaseResponse)
async def update_case(
    case_id: UUID,
    case_data: LegalCaseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("legal:update"))
):
    legal_service = LegalService(db)
    case = await legal_service.update_case(case_id, case_data)
    if not case:
        raise HTTPException(status_code=404, detail="Legal case not found")
    return case


@router.delete("/cases/{case_id}")
async def delete_case(
    case_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("legal:delete"))
):
    legal_service = LegalService(db)
    success = await legal_service.delete_case(case_id)
    if not success:
        raise HTTPException(status_code=404, detail="Legal case not found")
    return {"message": "Legal case deleted successfully"}


@router.get("/lawyers")
async def list_lawyers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("legal:read"))
):
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/lawyers", status_code=status.HTTP_201_CREATED)
async def create_lawyer(
    lawyer_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("legal:create"))
):
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/hearings")
async def list_hearings(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    case_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("legal:read"))
):
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/hearings", status_code=status.HTTP_201_CREATED)
async def create_hearing(
    hearing_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("legal:create"))
):
    raise HTTPException(status_code=501, detail="Not implemented")
