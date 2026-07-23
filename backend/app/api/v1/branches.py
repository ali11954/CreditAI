from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from app.database import get_db
from app.models.core import Branch
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user, require_permission


class BranchCreate(BaseModel):
    company_id: UUID
    name: str
    name_ar: Optional[str] = None
    code: str
    address: Optional[str] = None
    phone: Optional[str] = None


class BranchUpdate(BaseModel):
    name: Optional[str] = None
    name_ar: Optional[str] = None
    code: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class BranchResponse(BaseModel):
    id: UUID
    company_id: UUID
    name: str
    name_ar: Optional[str] = None
    code: str
    address: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


router = APIRouter()


@router.get("/", response_model=PaginatedResponse[BranchResponse])
async def list_branches(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    company_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("branches:read"))
):
    query = select(Branch)
    if search:
        query = query.where(
            (Branch.name.ilike(f"%{search}%")) |
            (Branch.code.ilike(f"%{search}%"))
        )
    if company_id:
        query = query.where(Branch.company_id == company_id)

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


@router.get("/{branch_id}", response_model=BranchResponse)
async def get_branch(
    branch_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("branches:read"))
):
    result = await db.execute(select(Branch).where(Branch.id == branch_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Branch not found")
    return item


@router.post("/", response_model=BranchResponse, status_code=status.HTTP_201_CREATED)
async def create_branch(
    branch_data: BranchCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("branches:create"))
):
    item = Branch(
        company_id=branch_data.company_id,
        name=branch_data.name,
        name_ar=branch_data.name_ar,
        code=branch_data.code,
        address=branch_data.address,
        phone=branch_data.phone
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.put("/{branch_id}", response_model=BranchResponse)
async def update_branch(
    branch_id: UUID,
    branch_data: BranchUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("branches:update"))
):
    result = await db.execute(select(Branch).where(Branch.id == branch_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Branch not found")

    update_data = branch_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    await db.flush()
    await db.refresh(item)
    return item


@router.delete("/{branch_id}")
async def delete_branch(
    branch_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("branches:delete"))
):
    result = await db.execute(select(Branch).where(Branch.id == branch_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Branch not found")

    item.is_active = False
    await db.flush()
    return {"message": "Branch deleted successfully"}
