from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from uuid import UUID

from app.database import get_db
from app.models.core import Currency
from app.schemas.currency import CurrencyCreate, CurrencyUpdate, CurrencyResponse
from app.schemas.common import PaginatedResponse, MessageResponse
from app.dependencies import get_current_user

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[CurrencyResponse])
async def list_currencies(
    page: int = 1,
    limit: int = 50,
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = select(Currency)
    count_query = select(func.count(Currency.id))

    if search:
        query = query.where(
            (Currency.code.ilike(f"%{search}%")) |
            (Currency.name.ilike(f"%{search}%")) |
            (Currency.name_ar.ilike(f"%{search}%"))
        )
        count_query = count_query.where(
            (Currency.code.ilike(f"%{search}%")) |
            (Currency.name.ilike(f"%{search}%")) |
            (Currency.name_ar.ilike(f"%{search}%"))
        )

    if is_active is not None:
        query = query.where(Currency.is_active == is_active)
        count_query = count_query.where(Currency.is_active == is_active)

    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = query.order_by(Currency.code)
    query = query.offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()

    return PaginatedResponse(
        items=[CurrencyResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=limit,
        total_pages=(total + limit - 1) // limit
    )


@router.get("/active", response_model=list[CurrencyResponse])
async def list_active_currencies(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = select(Currency).where(Currency.is_active == True).order_by(Currency.code)
    result = await db.execute(query)
    items = result.scalars().all()
    return [CurrencyResponse.model_validate(item) for item in items]


@router.get("/{currency_id}", response_model=CurrencyResponse)
async def get_currency(
    currency_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = await db.execute(select(Currency).where(Currency.id == currency_id))
    currency = result.scalar_one_or_none()
    if not currency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found")
    return CurrencyResponse.model_validate(currency)


@router.get("/code/{code}", response_model=CurrencyResponse)
async def get_currency_by_code(
    code: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = await db.execute(select(Currency).where(Currency.code == code.upper()))
    currency = result.scalar_one_or_none()
    if not currency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found")
    return CurrencyResponse.model_validate(currency)


@router.post("/", response_model=CurrencyResponse, status_code=status.HTTP_201_CREATED)
async def create_currency(
    data: CurrencyCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    existing = await db.execute(select(Currency).where(Currency.code == data.code.upper()))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Currency code already exists")

    currency = Currency(
        code=data.code.upper(),
        name=data.name,
        name_ar=data.name_ar,
        symbol=data.symbol,
        is_base=data.is_base,
        exchange_rate=data.exchange_rate,
        is_active=data.is_active
    )
    db.add(currency)
    await db.commit()
    await db.refresh(currency)
    return CurrencyResponse.model_validate(currency)


@router.put("/{currency_id}", response_model=CurrencyResponse)
async def update_currency(
    currency_id: UUID,
    data: CurrencyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = await db.execute(select(Currency).where(Currency.id == currency_id))
    currency = result.scalar_one_or_none()
    if not currency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found")

    update_data = data.model_dump(exclude_unset=True)
    if "code" in update_data:
        update_data["code"] = update_data["code"].upper()
        existing = await db.execute(
            select(Currency).where(Currency.code == update_data["code"], Currency.id != currency_id)
        )
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Currency code already exists")

    for key, value in update_data.items():
        setattr(currency, key, value)

    await db.commit()
    await db.refresh(currency)
    return CurrencyResponse.model_validate(currency)


@router.delete("/{currency_id}", response_model=MessageResponse)
async def delete_currency(
    currency_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = await db.execute(select(Currency).where(Currency.id == currency_id))
    currency = result.scalar_one_or_none()
    if not currency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found")

    if currency.is_base:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete base currency")

    currency.is_active = False
    await db.commit()
    return MessageResponse(message="Currency deactivated successfully")
