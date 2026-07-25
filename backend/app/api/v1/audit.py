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
    from app.models.audit import AIDecisionLog
    from sqlalchemy import select, func
    query = select(AIDecisionLog).where(AIDecisionLog.is_active == True)
    count_query = select(func.count(AIDecisionLog.id)).where(AIDecisionLog.is_active == True)
    if model_name:
        query = query.where(AIDecisionLog.model_name == model_name)
        count_query = count_query.where(AIDecisionLog.model_name == model_name)
    total = (await db.execute(count_query)).scalar() or 0
    query = query.order_by(AIDecisionLog.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    decisions = [dict(row._mapping) for row in result.all()]
    return PaginatedResponse(items=decisions, total=total, page=page, page_size=page_size, total_pages=(total + page_size - 1) // page_size)


@router.get("/security-events")
async def list_security_events(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    event_type: Optional[str] = None,
    severity: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("audit:read"))
):
    from app.models.audit import SecurityEvent
    from sqlalchemy import select, func
    query = select(SecurityEvent).where(SecurityEvent.is_active == True)
    count_query = select(func.count(SecurityEvent.id)).where(SecurityEvent.is_active == True)
    if event_type:
        query = query.where(SecurityEvent.event_type == event_type)
        count_query = count_query.where(SecurityEvent.event_type == event_type)
    if severity:
        query = query.where(SecurityEvent.severity == severity)
        count_query = count_query.where(SecurityEvent.severity == severity)
    total = (await db.execute(count_query)).scalar() or 0
    query = query.order_by(SecurityEvent.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    events = [dict(row._mapping) for row in result.all()]
    return PaginatedResponse(items=events, total=total, page=page, page_size=page_size, total_pages=(total + page_size - 1) // page_size)
