from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from app.database import get_db
from app.models.exposure import Exposure, ConcentrationLimit, StressTest
from app.schemas.exposure import (
    ExposureCreate, ExposureUpdate, ExposureResponse,
    ConcentrationLimitCreate, ConcentrationLimitUpdate, ConcentrationLimitResponse,
    StressTestCreate, StressTestUpdate, StressTestResponse
)
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user, require_permission

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[ExposureResponse])
async def list_exposures(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    customer_id: Optional[UUID] = None,
    exposure_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    query = select(Exposure)
    if customer_id:
        query = query.where(Exposure.customer_id == customer_id)
    if exposure_type:
        query = query.where(Exposure.exposure_type == exposure_type)

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


@router.get("/{exposure_id}", response_model=ExposureResponse)
async def get_exposure(
    exposure_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    result = await db.execute(select(Exposure).where(Exposure.id == exposure_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Exposure not found")
    return item


@router.post("/", response_model=ExposureResponse, status_code=status.HTTP_201_CREATED)
async def create_exposure(
    exposure_data: ExposureCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:create"))
):
    item = Exposure(
        customer_id=exposure_data.customer_id,
        exposure_type=exposure_data.exposure_type,
        amount=exposure_data.amount,
        currency_id=exposure_data.currency_id,
        details=exposure_data.details
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.put("/{exposure_id}", response_model=ExposureResponse)
async def update_exposure(
    exposure_id: UUID,
    exposure_data: ExposureUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:update"))
):
    result = await db.execute(select(Exposure).where(Exposure.id == exposure_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Exposure not found")

    update_data = exposure_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    item.calculated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(item)
    return item


@router.delete("/{exposure_id}")
async def delete_exposure(
    exposure_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:delete"))
):
    result = await db.execute(select(Exposure).where(Exposure.id == exposure_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Exposure not found")

    item.is_active = False
    await db.flush()
    return {"message": "Exposure deleted successfully"}


@router.get("/concentration-limits", response_model=PaginatedResponse[ConcentrationLimitResponse])
async def list_concentration_limits(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    concentration_type: Optional[str] = None,
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    query = select(ConcentrationLimit)
    if concentration_type:
        query = query.where(ConcentrationLimit.concentration_type == concentration_type)
    if category:
        query = query.where(ConcentrationLimit.category == category)

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


@router.get("/concentration-limits/{limit_id}", response_model=ConcentrationLimitResponse)
async def get_concentration_limit(
    limit_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    result = await db.execute(select(ConcentrationLimit).where(ConcentrationLimit.id == limit_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Concentration limit not found")
    return item


@router.post("/concentration-limits", response_model=ConcentrationLimitResponse, status_code=status.HTTP_201_CREATED)
async def create_concentration_limit(
    limit_data: ConcentrationLimitCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:create"))
):
    item = ConcentrationLimit(
        concentration_type=limit_data.concentration_type,
        category=limit_data.category,
        limit_amount=limit_data.limit_amount,
        utilized_amount=limit_data.utilized_amount,
        currency_id=limit_data.currency_id,
        threshold_percentage=limit_data.threshold_percentage
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.put("/concentration-limits/{limit_id}", response_model=ConcentrationLimitResponse)
async def update_concentration_limit(
    limit_id: UUID,
    limit_data: ConcentrationLimitUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:update"))
):
    result = await db.execute(select(ConcentrationLimit).where(ConcentrationLimit.id == limit_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Concentration limit not found")

    update_data = limit_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    await db.flush()
    await db.refresh(item)
    return item


@router.delete("/concentration-limits/{limit_id}")
async def delete_concentration_limit(
    limit_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:delete"))
):
    result = await db.execute(select(ConcentrationLimit).where(ConcentrationLimit.id == limit_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Concentration limit not found")

    item.is_active = False
    await db.flush()
    return {"message": "Concentration limit deleted successfully"}


@router.get("/stress-tests", response_model=PaginatedResponse[StressTestResponse])
async def list_stress_tests(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    query = select(StressTest)

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


@router.get("/stress-tests/{test_id}", response_model=StressTestResponse)
async def get_stress_test(
    test_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    result = await db.execute(select(StressTest).where(StressTest.id == test_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Stress test not found")
    return item


@router.post("/stress-tests", response_model=StressTestResponse, status_code=status.HTTP_201_CREATED)
async def create_stress_test(
    test_data: StressTestCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:create"))
):
    item = StressTest(
        name=test_data.name,
        description=test_data.description,
        scenario=test_data.scenario,
        results=test_data.results,
        conducted_by=current_user.id
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.put("/stress-tests/{test_id}", response_model=StressTestResponse)
async def update_stress_test(
    test_id: UUID,
    test_data: StressTestUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:update"))
):
    result = await db.execute(select(StressTest).where(StressTest.id == test_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Stress test not found")

    update_data = test_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    await db.flush()
    await db.refresh(item)
    return item


@router.delete("/stress-tests/{test_id}")
async def delete_stress_test(
    test_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:delete"))
):
    result = await db.execute(select(StressTest).where(StressTest.id == test_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Stress test not found")

    item.is_active = False
    await db.flush()
    return {"message": "Stress test deleted successfully"}
