from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from app.database import get_db
from app.models.customer import Customer
from app.models.compliance import KYCRecord
from app.dependencies import get_current_active_user, require_permission

router = APIRouter()


class OnboardingStatusResponse(BaseModel):
    customer_id: UUID
    onboarding_status: str
    kyc_status: str
    status: str
    completed_steps: List[str] = []
    current_step: Optional[str] = None

    class Config:
        from_attributes = True


class CompleteStepRequest(BaseModel):
    step: str


class KYCVerifyRequest(BaseModel):
    documents: List[dict] = []


class KYCStatusResponse(BaseModel):
    customer_id: UUID
    kyc_status: str
    records: List[dict] = []

    class Config:
        from_attributes = True


@router.get("/{customer_id}/onboarding-status", response_model=OnboardingStatusResponse)
async def get_onboarding_status(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("customers:read"))
):
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    metadata = customer.extra_data or {}
    completed_steps = metadata.get("onboarding_steps", [])

    steps = ["registration", "documents", "kyc", "credit_assessment", "approval"]
    current_step = None
    for step in steps:
        if step not in completed_steps:
            current_step = step
            break

    return OnboardingStatusResponse(
        customer_id=customer.id,
        onboarding_status=customer.onboarding_status,
        kyc_status=customer.kyc_status,
        status=customer.status,
        completed_steps=completed_steps,
        current_step=current_step
    )


@router.post("/{customer_id}/start-onboarding", response_model=OnboardingStatusResponse)
async def start_onboarding(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("customers:update"))
):
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer.onboarding_status = "in_progress"
    customer.status = "active"

    metadata = customer.extra_data or {}
    metadata["onboarding_started_at"] = datetime.utcnow().isoformat()
    metadata["onboarding_steps"] = []
    customer.extra_data = metadata

    await db.flush()
    await db.refresh(customer)

    return OnboardingStatusResponse(
        customer_id=customer.id,
        onboarding_status=customer.onboarding_status,
        kyc_status=customer.kyc_status,
        status=customer.status,
        completed_steps=[],
        current_step="registration"
    )


@router.post("/{customer_id}/complete-step", response_model=OnboardingStatusResponse)
async def complete_onboarding_step(
    customer_id: UUID,
    request: CompleteStepRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("customers:update"))
):
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    valid_steps = ["registration", "documents", "kyc", "credit_assessment", "approval"]
    if request.step not in valid_steps:
        raise HTTPException(status_code=400, detail=f"Invalid step. Valid steps: {valid_steps}")

    metadata = customer.extra_data or {}
    completed_steps = metadata.get("onboarding_steps", [])

    if request.step not in completed_steps:
        completed_steps.append(request.step)
        metadata["onboarding_steps"] = completed_steps
        metadata[f"{request.step}_completed_at"] = datetime.utcnow().isoformat()
        customer.extra_data = metadata

    if len(completed_steps) == len(valid_steps):
        customer.onboarding_status = "completed"
        customer.status = "active"
        metadata["onboarding_completed_at"] = datetime.utcnow().isoformat()
        customer.extra_data = metadata
    elif request.step == "kyc":
        customer.kyc_status = "pending"

    await db.flush()
    await db.refresh(customer)

    steps = ["registration", "documents", "kyc", "credit_assessment", "approval"]
    current_step = None
    for step in steps:
        if step not in completed_steps:
            current_step = step
            break

    return OnboardingStatusResponse(
        customer_id=customer.id,
        onboarding_status=customer.onboarding_status,
        kyc_status=customer.kyc_status,
        status=customer.status,
        completed_steps=completed_steps,
        current_step=current_step
    )


@router.get("/{customer_id}/kyc", response_model=KYCStatusResponse)
async def get_kyc_status(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("customers:read"))
):
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    kyc_result = await db.execute(
        select(KYCRecord)
        .where(KYCRecord.customer_id == customer_id)
        .where(KYCRecord.is_active == True)
        .order_by(KYCRecord.created_at.desc())
    )
    records = kyc_result.scalars().all()

    return KYCStatusResponse(
        customer_id=customer.id,
        kyc_status=customer.kyc_status,
        records=[
            {
                "id": str(r.id),
                "type": r.record_type,
                "status": r.status,
                "verified_at": r.verified_at.isoformat() if r.verified_at else None,
                "expires_at": r.expires_at.isoformat() if r.expires_at else None,
            }
            for r in records
        ]
    )


@router.post("/{customer_id}/kyc/verify")
async def verify_kyc(
    customer_id: UUID,
    request: KYCVerifyRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("compliance:update"))
):
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    kyc_record = KYCRecord(
        customer_id=customer_id,
        record_type="identity",
        status="verified",
        verified_by=current_user.id,
        verified_at=datetime.utcnow(),
        documents=request.documents
    )
    db.add(kyc_record)

    customer.kyc_status = "verified"

    metadata = customer.extra_data or {}
    metadata["kyc_verified_at"] = datetime.utcnow().isoformat()
    metadata["kyc_verified_by"] = str(current_user.id)
    customer.extra_data = metadata

    await db.flush()
    await db.refresh(kyc_record)

    return {
        "message": "KYC verification completed",
        "customer_id": str(customer_id),
        "kyc_record_id": str(kyc_record.id),
        "status": "verified"
    }
