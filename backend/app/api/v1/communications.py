from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from app.database import get_db
from app.models.communication import CommunicationTemplate, CommunicationLog, Campaign
from app.schemas.communication import (
    CommunicationTemplateCreate, CommunicationTemplateUpdate, CommunicationTemplateResponse,
    CommunicationLogCreate, CommunicationLogUpdate, CommunicationLogResponse,
    CampaignCreate, CampaignUpdate, CampaignResponse
)
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user, require_permission

router = APIRouter()


@router.get("/templates", response_model=PaginatedResponse[CommunicationTemplateResponse])
async def list_templates(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    type_filter: Optional[str] = Query(None, alias="type"),
    company_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("communications:read"))
):
    query = select(CommunicationTemplate)
    if type_filter:
        query = query.where(CommunicationTemplate.template_type == type_filter)
    if company_id:
        query = query.where(CommunicationTemplate.company_id == company_id)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    items = result.scalars().all()

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


@router.get("/templates/{template_id}", response_model=CommunicationTemplateResponse)
async def get_template(
    template_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("communications:read"))
):
    result = await db.execute(select(CommunicationTemplate).where(CommunicationTemplate.id == template_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Template not found")
    return item


@router.post("/templates", response_model=CommunicationTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    template_data: CommunicationTemplateCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("communications:create"))
):
    item = CommunicationTemplate(
        name=template_data.name,
        name_ar=template_data.name_ar,
        template_type=template_data.type,
        subject=template_data.subject,
        body=template_data.body,
        variables=template_data.variables,
        is_active=template_data.is_active,
        company_id=template_data.company_id
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.put("/templates/{template_id}", response_model=CommunicationTemplateResponse)
async def update_template(
    template_id: UUID,
    template_data: CommunicationTemplateUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("communications:update"))
):
    result = await db.execute(select(CommunicationTemplate).where(CommunicationTemplate.id == template_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Template not found")

    update_data = template_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "type":
            setattr(item, "template_type", value)
        else:
            setattr(item, key, value)

    await db.flush()
    await db.refresh(item)
    return item


@router.delete("/templates/{template_id}")
async def delete_template(
    template_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("communications:delete"))
):
    result = await db.execute(select(CommunicationTemplate).where(CommunicationTemplate.id == template_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Template not found")

    item.is_active = False
    await db.flush()
    return {"message": "Template deleted successfully"}


@router.get("/logs", response_model=PaginatedResponse[CommunicationLogResponse])
async def list_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    customer_id: Optional[UUID] = None,
    type_filter: Optional[str] = Query(None, alias="type"),
    status_filter: Optional[str] = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("communications:read"))
):
    query = select(CommunicationLog)
    if customer_id:
        query = query.where(CommunicationLog.customer_id == customer_id)
    if type_filter:
        query = query.where(CommunicationLog.log_type == type_filter)
    if status_filter:
        query = query.where(CommunicationLog.status == status_filter)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    items = result.scalars().all()

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


@router.get("/logs/{log_id}", response_model=CommunicationLogResponse)
async def get_log(
    log_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("communications:read"))
):
    result = await db.execute(select(CommunicationLog).where(CommunicationLog.id == log_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Communication log not found")
    return item


@router.post("/send", response_model=CommunicationLogResponse, status_code=status.HTTP_201_CREATED)
async def send_communication(
    log_data: CommunicationLogCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("communications:create"))
):
    item = CommunicationLog(
        customer_id=log_data.customer_id,
        log_type=log_data.type,
        direction=log_data.direction,
        recipient=log_data.recipient,
        subject=log_data.subject,
        content=log_data.content,
        status=log_data.status,
        sent_at=log_data.sent_at,
        created_by=current_user.id
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.get("/campaigns", response_model=PaginatedResponse[CampaignResponse])
async def list_campaigns(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    company_id: Optional[UUID] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("communications:read"))
):
    query = select(Campaign)
    if company_id:
        query = query.where(Campaign.company_id == company_id)
    if status_filter:
        query = query.where(Campaign.status == status_filter)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    items = result.scalars().all()

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


@router.get("/campaigns/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("communications:read"))
):
    result = await db.execute(select(Campaign).where(Campaign.id == campaign_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return item


@router.post("/campaigns", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    campaign_data: CampaignCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("communications:create"))
):
    item = Campaign(
        name=campaign_data.name,
        campaign_type=campaign_data.type,
        target_audience=campaign_data.target_audience,
        template_id=campaign_data.template_id,
        scheduled_date=campaign_data.scheduled_date,
        status=campaign_data.status,
        sent_count=campaign_data.sent_count,
        opened_count=campaign_data.opened_count,
        company_id=campaign_data.company_id
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.put("/campaigns/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: UUID,
    campaign_data: CampaignUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("communications:update"))
):
    result = await db.execute(select(Campaign).where(Campaign.id == campaign_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Campaign not found")

    update_data = campaign_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "type":
            setattr(item, "campaign_type", value)
        else:
            setattr(item, key, value)

    await db.flush()
    await db.refresh(item)
    return item


@router.delete("/campaigns/{campaign_id}")
async def delete_campaign(
    campaign_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("communications:delete"))
):
    result = await db.execute(select(Campaign).where(Campaign.id == campaign_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Campaign not found")

    item.is_active = False
    await db.flush()
    return {"message": "Campaign deleted successfully"}
