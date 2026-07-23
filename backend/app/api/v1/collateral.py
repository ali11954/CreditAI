from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from decimal import Decimal

from app.database import get_db
from app.models.collateral import Collateral, CollateralValuation, CollateralRelease
from app.schemas.collateral import (
    CollateralCreate, CollateralUpdate, CollateralResponse,
    CollateralValuationCreate, CollateralValuationResponse,
    CollateralReleaseCreate, CollateralReleaseResponse
)
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user, require_permission

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[CollateralResponse])
async def list_collaterals(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    customer_id: Optional[UUID] = None,
    collateral_type: Optional[str] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    query = select(Collateral)
    if customer_id:
        query = query.where(Collateral.customer_id == customer_id)
    if collateral_type:
        query = query.where(Collateral.collateral_type == collateral_type)
    if status_filter:
        query = query.where(Collateral.status == status_filter)

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


@router.get("/{collateral_id}", response_model=CollateralResponse)
async def get_collateral(
    collateral_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    result = await db.execute(select(Collateral).where(Collateral.id == collateral_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Collateral not found")
    return item


@router.post("/", response_model=CollateralResponse, status_code=status.HTTP_201_CREATED)
async def create_collateral(
    collateral_data: CollateralCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:create"))
):
    item = Collateral(
        customer_id=collateral_data.customer_id,
        collateral_type=collateral_data.type,
        description=collateral_data.description,
        estimated_value=collateral_data.estimated_value,
        assessed_value=collateral_data.assessed_value,
        currency_id=collateral_data.currency_id,
        status=collateral_data.status,
        registration_number=collateral_data.registration_number,
        location=collateral_data.location,
        expiry_date=collateral_data.expiry_date,
        insurance_required=collateral_data.insurance_required,
        notes=collateral_data.notes,
        images=collateral_data.images
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.put("/{collateral_id}", response_model=CollateralResponse)
async def update_collateral(
    collateral_id: UUID,
    collateral_data: CollateralUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:update"))
):
    result = await db.execute(select(Collateral).where(Collateral.id == collateral_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Collateral not found")

    update_data = collateral_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "type":
            setattr(item, "collateral_type", value)
        else:
            setattr(item, key, value)

    await db.flush()
    await db.refresh(item)
    return item


@router.delete("/{collateral_id}")
async def delete_collateral(
    collateral_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:delete"))
):
    result = await db.execute(select(Collateral).where(Collateral.id == collateral_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Collateral not found")

    item.is_active = False
    await db.flush()
    return {"message": "Collateral deleted successfully"}


@router.post("/{collateral_id}/valuation", response_model=CollateralValuationResponse, status_code=status.HTTP_201_CREATED)
async def add_valuation(
    collateral_id: UUID,
    valuation_data: CollateralValuationCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:create"))
):
    result = await db.execute(select(Collateral).where(Collateral.id == collateral_id))
    collateral = result.scalar_one_or_none()
    if not collateral:
        raise HTTPException(status_code=404, detail="Collateral not found")

    valuation = CollateralValuation(
        collateral_id=collateral_id,
        valuation_date=valuation_data.valuation_date,
        value=valuation_data.value,
        methodology=valuation_data.methodology,
        valuator=valuation_data.valuator,
        next_valuation_date=valuation_data.next_valuation_date
    )
    db.add(valuation)

    collateral.assessed_value = valuation_data.value
    await db.flush()
    await db.refresh(valuation)
    return valuation


@router.get("/{collateral_id}/valuations", response_model=List[CollateralValuationResponse])
async def get_valuations(
    collateral_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    result = await db.execute(
        select(CollateralValuation)
        .where(CollateralValuation.collateral_id == collateral_id)
        .where(CollateralValuation.is_active == True)
        .order_by(CollateralValuation.valuation_date.desc())
    )
    return result.scalars().all()


@router.post("/{collateral_id}/release", response_model=CollateralReleaseResponse, status_code=status.HTTP_201_CREATED)
async def release_collateral(
    collateral_id: UUID,
    release_data: CollateralReleaseCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:update"))
):
    result = await db.execute(select(Collateral).where(Collateral.id == collateral_id))
    collateral = result.scalar_one_or_none()
    if not collateral:
        raise HTTPException(status_code=404, detail="Collateral not found")

    release = CollateralRelease(
        collateral_id=collateral_id,
        released_by=current_user.id,
        released_at=release_data.released_at,
        reason=release_data.reason,
        approved_by=release_data.approved_by
    )
    db.add(release)

    collateral.status = "released"
    await db.flush()
    await db.refresh(release)
    return release
