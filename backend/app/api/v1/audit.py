from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

from app.database import get_db
from app.services.audit_service import AuditService
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user, require_permission

router = APIRouter()


@router.get("/trail")
async def list_audit_trail(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user_id: Optional[UUID] = None,
    entity_type: Optional[str] = None,
    entity_id: Optional[UUID] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("audit:read"))
):
    audit_service = AuditService(db)
    logs, total = await audit_service.get_audit_trail(
        page=page,
        page_size=page_size,
        user_id=user_id,
        entity_type=entity_type,
        entity_id=entity_id
    )
    return PaginatedResponse(
        items=logs,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


@router.get("/ai-decisions")
async def list_ai_decisions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    model_name: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("audit:read"))
):
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/security-events")
async def list_security_events(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    event_type: Optional[str] = None,
    severity: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("audit:read"))
):
    raise HTTPException(status_code=501, detail="Not implemented")
