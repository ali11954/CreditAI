from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

from app.database import get_db
from app.services.sap_service import SAPService
from app.dependencies import get_current_active_user, require_permission

router = APIRouter()


@router.get("/sync-status")
async def get_sync_status(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("sap:read"))
):
    sap_service = SAPService(db)
    status = await sap_service.get_sync_status()
    return status


@router.post("/sync/{entity_type}/{entity_id}")
async def sync_entity(
    entity_type: str,
    entity_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("sap:sync"))
):
    sap_service = SAPService(db)
    result = await sap_service.sync_entity(entity_type, entity_id)
    return result


@router.get("/business-partners")
async def list_business_partners(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("sap:read"))
):
    from app.models.sap import SAPBusinessPartner
    from sqlalchemy import select, func
    query = select(SAPBusinessPartner).where(SAPBusinessPartner.is_active == True)
    count_query = select(func.count(SAPBusinessPartner.id)).where(SAPBusinessPartner.is_active == True)
    total = (await db.execute(count_query)).scalar() or 0
    query = query.order_by(SAPBusinessPartner.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    partners = [dict(row._mapping) for row in result.all()]
    return {"items": partners, "total": total, "page": page, "page_size": page_size}


@router.get("/invoices")
async def list_sap_invoices(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("sap:read"))
):
    from app.models.sap import SAPInvoice
    from sqlalchemy import select, func
    query = select(SAPInvoice).where(SAPInvoice.is_active == True)
    count_query = select(func.count(SAPInvoice.id)).where(SAPInvoice.is_active == True)
    total = (await db.execute(count_query)).scalar() or 0
    query = query.order_by(SAPInvoice.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    invoices = [dict(row._mapping) for row in result.all()]
    return {"items": invoices, "total": total, "page": page, "page_size": page_size}


@router.get("/sync-logs")
async def list_sync_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    entity_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("sap:read"))
):
    from app.models.sap import SAPSyncLog
    from sqlalchemy import select, func
    query = select(SAPSyncLog).where(SAPSyncLog.is_active == True)
    count_query = select(func.count(SAPSyncLog.id)).where(SAPSyncLog.is_active == True)
    if entity_type:
        query = query.where(SAPSyncLog.entity_type == entity_type)
        count_query = count_query.where(SAPSyncLog.entity_type == entity_type)
    total = (await db.execute(count_query)).scalar() or 0
    query = query.order_by(SAPSyncLog.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    logs = [dict(row._mapping) for row in result.all()]
    return {"items": logs, "total": total, "page": page, "page_size": page_size}


@router.post("/queue")
async def queue_sync(
    entity_type: str,
    entity_id: UUID,
    action: str,
    payload: dict = {},
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("sap:sync"))
):
    sap_service = SAPService(db)
    result = await sap_service.queue_sync(entity_type, entity_id, action, payload)
    return result
