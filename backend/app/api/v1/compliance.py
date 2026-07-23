from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from app.database import get_db
from app.models.compliance import (
    KYCRecord, AMLCheck, PEPCheck, SanctionCheck,
    ComplianceCase, DueDiligence
)
from app.schemas.compliance import (
    KYCRecordCreate, KYCRecordUpdate, KYCRecordResponse,
    AMLCheckCreate, AMLCheckResponse,
    PEPCheckCreate, PEPCheckResponse,
    SanctionCheckCreate, SanctionCheckResponse,
    ComplianceCaseCreate, ComplianceCaseUpdate, ComplianceCaseResponse,
    DueDiligenceCreate, DueDiligenceUpdate, DueDiligenceResponse
)
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user, require_permission

router = APIRouter()


@router.get("/kyc/{customer_id}", response_model=List[KYCRecordResponse])
async def get_kyc_records(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("compliance:read"))
):
    result = await db.execute(
        select(KYCRecord)
        .where(KYCRecord.customer_id == customer_id)
        .where(KYCRecord.is_active == True)
        .order_by(KYCRecord.created_at.desc())
    )
    return result.scalars().all()


@router.post("/kyc/{customer_id}", response_model=KYCRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_kyc_record(
    customer_id: UUID,
    record_data: KYCRecordCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("compliance:create"))
):
    record = KYCRecord(
        customer_id=customer_id,
        record_type=record_data.type,
        status=record_data.status,
        documents=record_data.documents,
        notes=record_data.notes
    )
    db.add(record)
    await db.flush()
    await db.refresh(record)
    return record


@router.put("/kyc/{record_id}", response_model=KYCRecordResponse)
async def update_kyc_record(
    record_id: UUID,
    record_data: KYCRecordUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("compliance:update"))
):
    result = await db.execute(select(KYCRecord).where(KYCRecord.id == record_id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="KYC record not found")

    update_data = record_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(record, key, value)

    await db.flush()
    await db.refresh(record)
    return record


@router.get("/aml/{customer_id}", response_model=List[AMLCheckResponse])
async def get_aml_checks(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("compliance:read"))
):
    result = await db.execute(
        select(AMLCheck)
        .where(AMLCheck.customer_id == customer_id)
        .where(AMLCheck.is_active == True)
        .order_by(AMLCheck.checked_at.desc())
    )
    return result.scalars().all()


@router.post("/aml/{customer_id}", response_model=AMLCheckResponse, status_code=status.HTTP_201_CREATED)
async def run_aml_check(
    customer_id: UUID,
    check_data: AMLCheckCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("compliance:create"))
):
    check = AMLCheck(
        customer_id=customer_id,
        check_type=check_data.check_type,
        result=check_data.result,
        score=check_data.score,
        details=check_data.details,
        checked_by=current_user.id
    )
    db.add(check)
    await db.flush()
    await db.refresh(check)
    return check


@router.get("/pep/{customer_id}", response_model=List[PEPCheckResponse])
async def get_pep_check(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("compliance:read"))
):
    result = await db.execute(
        select(PEPCheck)
        .where(PEPCheck.customer_id == customer_id)
        .where(PEPCheck.is_active == True)
        .order_by(PEPCheck.checked_at.desc())
    )
    return result.scalars().all()


@router.post("/pep/{customer_id}", response_model=PEPCheckResponse, status_code=status.HTTP_201_CREATED)
async def run_pep_check(
    customer_id: UUID,
    check_data: PEPCheckCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("compliance:create"))
):
    check = PEPCheck(
        customer_id=customer_id,
        is_pep=check_data.is_pep,
        pep_type=check_data.pep_type,
        details=check_data.details,
        checked_by=current_user.id
    )
    db.add(check)
    await db.flush()
    await db.refresh(check)
    return check


@router.get("/sanctions/{customer_id}", response_model=List[SanctionCheckResponse])
async def get_sanction_check(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("compliance:read"))
):
    result = await db.execute(
        select(SanctionCheck)
        .where(SanctionCheck.customer_id == customer_id)
        .where(SanctionCheck.is_active == True)
        .order_by(SanctionCheck.checked_at.desc())
    )
    return result.scalars().all()


@router.post("/sanctions/{customer_id}", response_model=SanctionCheckResponse, status_code=status.HTTP_201_CREATED)
async def run_sanction_check(
    customer_id: UUID,
    check_data: SanctionCheckCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("compliance:create"))
):
    check = SanctionCheck(
        customer_id=customer_id,
        is_sanctioned=check_data.is_sanctioned,
        list_name=check_data.list_name,
        details=check_data.details,
        checked_by=current_user.id
    )
    db.add(check)
    await db.flush()
    await db.refresh(check)
    return check


@router.get("/cases", response_model=PaginatedResponse[ComplianceCaseResponse])
async def list_compliance_cases(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    customer_id: Optional[UUID] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    priority: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("compliance:read"))
):
    query = select(ComplianceCase)
    if customer_id:
        query = query.where(ComplianceCase.customer_id == customer_id)
    if status_filter:
        query = query.where(ComplianceCase.status == status_filter)
    if priority:
        query = query.where(ComplianceCase.priority == priority)

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


@router.get("/cases/{case_id}", response_model=ComplianceCaseResponse)
async def get_compliance_case(
    case_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("compliance:read"))
):
    result = await db.execute(select(ComplianceCase).where(ComplianceCase.id == case_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Compliance case not found")
    return item


@router.post("/cases", response_model=ComplianceCaseResponse, status_code=status.HTTP_201_CREATED)
async def create_compliance_case(
    case_data: ComplianceCaseCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("compliance:create"))
):
    case = ComplianceCase(
        customer_id=case_data.customer_id,
        case_type=case_data.case_type,
        status=case_data.status,
        priority=case_data.priority,
        assigned_to=case_data.assigned_to,
        due_date=case_data.due_date,
        resolution=case_data.resolution,
        resolution_date=case_data.resolution_date,
        notes=case_data.notes
    )
    db.add(case)
    await db.flush()
    await db.refresh(case)
    return case


@router.put("/cases/{case_id}", response_model=ComplianceCaseResponse)
async def update_compliance_case(
    case_id: UUID,
    case_data: ComplianceCaseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("compliance:update"))
):
    result = await db.execute(select(ComplianceCase).where(ComplianceCase.id == case_id))
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Compliance case not found")

    update_data = case_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(case, key, value)

    await db.flush()
    await db.refresh(case)
    return case


@router.delete("/cases/{case_id}")
async def delete_compliance_case(
    case_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("compliance:delete"))
):
    result = await db.execute(select(ComplianceCase).where(ComplianceCase.id == case_id))
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Compliance case not found")

    case.is_active = False
    await db.flush()
    return {"message": "Compliance case deleted successfully"}


@router.get("/due-diligence/{customer_id}", response_model=List[DueDiligenceResponse])
async def get_due_diligence(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("compliance:read"))
):
    result = await db.execute(
        select(DueDiligence)
        .where(DueDiligence.customer_id == customer_id)
        .where(DueDiligence.is_active == True)
        .order_by(DueDiligence.created_at.desc())
    )
    return result.scalars().all()


@router.post("/due-diligence", response_model=DueDiligenceResponse, status_code=status.HTTP_201_CREATED)
async def create_due_diligence(
    data: DueDiligenceCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("compliance:create"))
):
    dd = DueDiligence(
        customer_id=data.customer_id,
        diligence_type=data.type,
        status=data.status,
        findings=data.findings,
        risk_level=data.risk_level,
        conducted_by=current_user.id
    )
    db.add(dd)
    await db.flush()
    await db.refresh(dd)
    return dd


@router.put("/due-diligence/{dd_id}", response_model=DueDiligenceResponse)
async def update_due_diligence(
    dd_id: UUID,
    data: DueDiligenceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("compliance:update"))
):
    result = await db.execute(select(DueDiligence).where(DueDiligence.id == dd_id))
    dd = result.scalar_one_or_none()
    if not dd:
        raise HTTPException(status_code=404, detail="Due diligence record not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(dd, key, value)

    await db.flush()
    await db.refresh(dd)
    return dd
