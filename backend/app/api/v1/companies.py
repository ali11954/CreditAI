from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from app.database import get_db
from app.models.core import Company
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user, require_permission


class CompanyCreate(BaseModel):
    name: str
    name_ar: Optional[str] = None
    registration_number: Optional[str] = None
    tax_id: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    logo: Optional[str] = None
    settings: dict = {}


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    name_ar: Optional[str] = None
    registration_number: Optional[str] = None
    tax_id: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    logo: Optional[str] = None
    settings: Optional[dict] = None
    is_active: Optional[bool] = None


class CompanyResponse(BaseModel):
    id: UUID
    name: str
    name_ar: Optional[str] = None
    registration_number: Optional[str] = None
    tax_id: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    logo: Optional[str] = None
    settings: dict = {}
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


router = APIRouter()


@router.get("/", response_model=PaginatedResponse[CompanyResponse])
async def list_companies(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("companies:read"))
):
    query = select(Company)
    if search:
        query = query.where(
            (Company.name.ilike(f"%{search}%")) |
            (Company.name_ar.ilike(f"%{search}%"))
        )

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


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("companies:read"))
):
    result = await db.execute(select(Company).where(Company.id == company_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Company not found")
    return item


@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    company_data: CompanyCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("companies:create"))
):
    item = Company(
        name=company_data.name,
        name_ar=company_data.name_ar,
        registration_number=company_data.registration_number,
        tax_id=company_data.tax_id,
        address=company_data.address,
        phone=company_data.phone,
        email=company_data.email,
        logo=company_data.logo,
        settings=company_data.settings
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: UUID,
    company_data: CompanyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("companies:update"))
):
    result = await db.execute(select(Company).where(Company.id == company_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Company not found")

    update_data = company_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    await db.flush()
    await db.refresh(item)
    return item


@router.delete("/{company_id}")
async def delete_company(
    company_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("companies:delete"))
):
    result = await db.execute(select(Company).where(Company.id == company_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Company not found")

    item.is_active = False
    await db.flush()
    return {"message": "Company deleted successfully"}
