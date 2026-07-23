from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from uuid import UUID
from decimal import Decimal

from app.database import get_db
from app.models.guarantor import Guarantor, GuarantorFinancial, GuarantorSupport
from app.schemas.guarantor import (
    GuarantorCreate, GuarantorUpdate, GuarantorResponse,
    GuarantorFinancialCreate, GuarantorFinancialResponse,
    GuarantorSupportCreate, GuarantorSupportResponse
)
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user, require_permission

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[GuarantorResponse])
async def list_guarantors(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    customer_id: Optional[UUID] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    query = select(Guarantor)
    if customer_id:
        query = query.where(Guarantor.customer_id == customer_id)
    if status_filter:
        query = query.where(Guarantor.status == status_filter)

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


@router.get("/{guarantor_id}", response_model=GuarantorResponse)
async def get_guarantor(
    guarantor_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    result = await db.execute(select(Guarantor).where(Guarantor.id == guarantor_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Guarantor not found")
    return item


@router.post("/", response_model=GuarantorResponse, status_code=status.HTTP_201_CREATED)
async def create_guarantor(
    guarantor_data: GuarantorCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:create"))
):
    item = Guarantor(
        customer_id=guarantor_data.customer_id,
        name=guarantor_data.name,
        name_ar=guarantor_data.name_ar,
        relationship_type=guarantor_data.relationship,
        guarantor_type=guarantor_data.type,
        is_individual=guarantor_data.is_individual,
        national_id=guarantor_data.national_id,
        commercial_register=guarantor_data.commercial_register,
        phone=guarantor_data.phone,
        email=guarantor_data.email,
        address=guarantor_data.address,
        status=guarantor_data.status
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.put("/{guarantor_id}", response_model=GuarantorResponse)
async def update_guarantor(
    guarantor_id: UUID,
    guarantor_data: GuarantorUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:update"))
):
    result = await db.execute(select(Guarantor).where(Guarantor.id == guarantor_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Guarantor not found")

    update_data = guarantor_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "relationship":
            setattr(item, "relationship_type", value)
        elif key == "type":
            setattr(item, "guarantor_type", value)
        else:
            setattr(item, key, value)

    await db.flush()
    await db.refresh(item)
    return item


@router.delete("/{guarantor_id}")
async def delete_guarantor(
    guarantor_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:delete"))
):
    result = await db.execute(select(Guarantor).where(Guarantor.id == guarantor_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Guarantor not found")

    item.is_active = False
    await db.flush()
    return {"message": "Guarantor deleted successfully"}


@router.get("/{guarantor_id}/financial", response_model=List[GuarantorFinancialResponse])
async def get_financial_assessments(
    guarantor_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    result = await db.execute(
        select(GuarantorFinancial)
        .where(GuarantorFinancial.guarantor_id == guarantor_id)
        .where(GuarantorFinancial.is_active == True)
        .order_by(GuarantorFinancial.assessment_date.desc())
    )
    return result.scalars().all()


@router.post("/{guarantor_id}/financial", response_model=GuarantorFinancialResponse, status_code=status.HTTP_201_CREATED)
async def create_financial_assessment(
    guarantor_id: UUID,
    financial_data: GuarantorFinancialCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:create"))
):
    result = await db.execute(select(Guarantor).where(Guarantor.id == guarantor_id))
    guarantor = result.scalar_one_or_none()
    if not guarantor:
        raise HTTPException(status_code=404, detail="Guarantor not found")

    item = GuarantorFinancial(
        guarantor_id=guarantor_id,
        assets=financial_data.assets,
        liabilities=financial_data.liabilities,
        income=financial_data.income,
        net_worth=financial_data.net_worth,
        assessment_date=financial_data.assessment_date,
        assessed_by=current_user.id
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.get("/{guarantor_id}/supports", response_model=List[GuarantorSupportResponse])
async def get_guarantor_supports(
    guarantor_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    result = await db.execute(
        select(GuarantorSupport)
        .where(GuarantorSupport.guarantor_id == guarantor_id)
        .where(GuarantorSupport.is_active == True)
        .order_by(GuarantorSupport.created_at.desc())
    )
    return result.scalars().all()


@router.post("/{guarantor_id}/supports", response_model=GuarantorSupportResponse, status_code=status.HTTP_201_CREATED)
async def create_guarantor_support(
    guarantor_id: UUID,
    support_data: GuarantorSupportCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:create"))
):
    result = await db.execute(select(Guarantor).where(Guarantor.id == guarantor_id))
    guarantor = result.scalar_one_or_none()
    if not guarantor:
        raise HTTPException(status_code=404, detail="Guarantor not found")

    item = GuarantorSupport(
        guarantor_id=guarantor_id,
        credit_application_id=support_data.credit_application_id,
        guarantee_type=support_data.guarantee_type,
        amount=support_data.amount,
        currency_id=support_data.currency_id,
        start_date=support_data.start_date,
        end_date=support_data.end_date,
        status=support_data.status
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item
