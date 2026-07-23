from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from uuid import UUID

from app.database import get_db
from app.models.insurance import InsuranceCompany, InsurancePolicy, InsuranceClaim
from app.schemas.insurance import (
    InsuranceCompanyCreate, InsuranceCompanyUpdate, InsuranceCompanyResponse,
    InsurancePolicyCreate, InsurancePolicyUpdate, InsurancePolicyResponse,
    InsuranceClaimCreate, InsuranceClaimUpdate, InsuranceClaimResponse
)
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user, require_permission

router = APIRouter()


@router.get("/companies", response_model=PaginatedResponse[InsuranceCompanyResponse])
async def list_insurance_companies(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("insurance:read"))
):
    query = select(InsuranceCompany)
    if search:
        query = query.where(InsuranceCompany.name.ilike(f"%{search}%"))

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


@router.get("/companies/{company_id}", response_model=InsuranceCompanyResponse)
async def get_insurance_company(
    company_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("insurance:read"))
):
    result = await db.execute(select(InsuranceCompany).where(InsuranceCompany.id == company_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Insurance company not found")
    return item


@router.post("/companies", response_model=InsuranceCompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_insurance_company(
    company_data: InsuranceCompanyCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("insurance:create"))
):
    item = InsuranceCompany(
        name=company_data.name,
        name_ar=company_data.name_ar,
        license_number=company_data.license_number,
        phone=company_data.phone,
        email=company_data.email,
        address=company_data.address
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.put("/companies/{company_id}", response_model=InsuranceCompanyResponse)
async def update_insurance_company(
    company_id: UUID,
    company_data: InsuranceCompanyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("insurance:update"))
):
    result = await db.execute(select(InsuranceCompany).where(InsuranceCompany.id == company_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Insurance company not found")

    update_data = company_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    await db.flush()
    await db.refresh(item)
    return item


@router.delete("/companies/{company_id}")
async def delete_insurance_company(
    company_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("insurance:delete"))
):
    result = await db.execute(select(InsuranceCompany).where(InsuranceCompany.id == company_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Insurance company not found")

    item.is_active = False
    await db.flush()
    return {"message": "Insurance company deleted successfully"}


@router.get("/policies", response_model=PaginatedResponse[InsurancePolicyResponse])
async def list_policies(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    customer_id: Optional[UUID] = None,
    insurance_company_id: Optional[UUID] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("insurance:read"))
):
    query = select(InsurancePolicy)
    if customer_id:
        query = query.where(InsurancePolicy.customer_id == customer_id)
    if insurance_company_id:
        query = query.where(InsurancePolicy.insurance_company_id == insurance_company_id)
    if status_filter:
        query = query.where(InsurancePolicy.status == status_filter)

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


@router.get("/policies/{policy_id}", response_model=InsurancePolicyResponse)
async def get_policy(
    policy_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("insurance:read"))
):
    result = await db.execute(select(InsurancePolicy).where(InsurancePolicy.id == policy_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Insurance policy not found")
    return item


@router.post("/policies", response_model=InsurancePolicyResponse, status_code=status.HTTP_201_CREATED)
async def create_policy(
    policy_data: InsurancePolicyCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("insurance:create"))
):
    item = InsurancePolicy(
        customer_id=policy_data.customer_id,
        insurance_company_id=policy_data.insurance_company_id,
        policy_number=policy_data.policy_number,
        policy_type=policy_data.policy_type,
        coverage_amount=policy_data.coverage_amount,
        premium=policy_data.premium,
        start_date=policy_data.start_date,
        end_date=policy_data.end_date,
        status=policy_data.status,
        documents=policy_data.documents
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.put("/policies/{policy_id}", response_model=InsurancePolicyResponse)
async def update_policy(
    policy_id: UUID,
    policy_data: InsurancePolicyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("insurance:update"))
):
    result = await db.execute(select(InsurancePolicy).where(InsurancePolicy.id == policy_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Insurance policy not found")

    update_data = policy_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    await db.flush()
    await db.refresh(item)
    return item


@router.delete("/policies/{policy_id}")
async def delete_policy(
    policy_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("insurance:delete"))
):
    result = await db.execute(select(InsurancePolicy).where(InsurancePolicy.id == policy_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Insurance policy not found")

    item.is_active = False
    await db.flush()
    return {"message": "Insurance policy deleted successfully"}


@router.get("/claims", response_model=PaginatedResponse[InsuranceClaimResponse])
async def list_claims(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    policy_id: Optional[UUID] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("insurance:read"))
):
    query = select(InsuranceClaim)
    if policy_id:
        query = query.where(InsuranceClaim.policy_id == policy_id)
    if status_filter:
        query = query.where(InsuranceClaim.status == status_filter)

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


@router.get("/claims/{claim_id}", response_model=InsuranceClaimResponse)
async def get_claim(
    claim_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("insurance:read"))
):
    result = await db.execute(select(InsuranceClaim).where(InsuranceClaim.id == claim_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Insurance claim not found")
    return item


@router.post("/claims", response_model=InsuranceClaimResponse, status_code=status.HTTP_201_CREATED)
async def create_claim(
    claim_data: InsuranceClaimCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("insurance:create"))
):
    item = InsuranceClaim(
        policy_id=claim_data.policy_id,
        claim_number=claim_data.claim_number,
        claim_date=claim_data.claim_date,
        amount=claim_data.amount,
        status=claim_data.status,
        description=claim_data.description,
        resolution=claim_data.resolution,
        resolved_date=claim_data.resolved_date
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.put("/claims/{claim_id}", response_model=InsuranceClaimResponse)
async def update_claim(
    claim_id: UUID,
    claim_data: InsuranceClaimUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("insurance:update"))
):
    result = await db.execute(select(InsuranceClaim).where(InsuranceClaim.id == claim_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Insurance claim not found")

    update_data = claim_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    await db.flush()
    await db.refresh(item)
    return item


@router.delete("/claims/{claim_id}")
async def delete_claim(
    claim_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("insurance:delete"))
):
    result = await db.execute(select(InsuranceClaim).where(InsuranceClaim.id == claim_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Insurance claim not found")

    item.is_active = False
    await db.flush()
    return {"message": "Insurance claim deleted successfully"}
