from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from app.database import get_db
from app.models.core import Department
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user, require_permission


class DepartmentCreate(BaseModel):
    company_id: UUID
    name: str
    name_ar: Optional[str] = None
    code: str


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    name_ar: Optional[str] = None
    code: Optional[str] = None
    is_active: Optional[bool] = None


class DepartmentResponse(BaseModel):
    id: UUID
    company_id: UUID
    name: str
    name_ar: Optional[str] = None
    code: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[DepartmentResponse])
async def list_departments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    company_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("departments:read"))
):
    query = select(Department)
    if search:
        query = query.where(
            (Department.name.ilike(f"%{search}%")) |
            (Department.code.ilike(f"%{search}%"))
        )
    if company_id:
        query = query.where(Department.company_id == company_id)

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


@router.get("/{department_id}", response_model=DepartmentResponse)
async def get_department(
    department_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("departments:read"))
):
    result = await db.execute(select(Department).where(Department.id == department_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Department not found")
    return item


@router.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(
    department_data: DepartmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("departments:create"))
):
    item = Department(
        company_id=department_data.company_id,
        name=department_data.name,
        name_ar=department_data.name_ar,
        code=department_data.code
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.put("/{department_id}", response_model=DepartmentResponse)
async def update_department(
    department_id: UUID,
    department_data: DepartmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("departments:update"))
):
    result = await db.execute(select(Department).where(Department.id == department_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Department not found")

    update_data = department_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    await db.flush()
    await db.refresh(item)
    return item


@router.delete("/{department_id}")
async def delete_department(
    department_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("departments:delete"))
):
    result = await db.execute(select(Department).where(Department.id == department_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Department not found")

    item.is_active = False
    await db.flush()
    return {"message": "Department deleted successfully"}
