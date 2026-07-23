from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from app.database import get_db
from app.models.credit import CreditCommittee, CommitteeMember, CommitteeDecision
from app.schemas.credit import (
    CreditCommitteeCreate, CreditCommitteeUpdate, CreditCommitteeResponse,
    CommitteeMemberCreate, CommitteeMemberResponse,
    CommitteeDecisionCreate, CommitteeDecisionUpdate, CommitteeDecisionResponse
)
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user, require_permission

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[CreditCommitteeResponse])
async def list_committees(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    company_id: Optional[UUID] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    query = select(CreditCommittee)
    if company_id:
        query = query.where(CreditCommittee.company_id == company_id)
    if status_filter:
        query = query.where(CreditCommittee.status == status_filter)

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


@router.get("/{committee_id}", response_model=CreditCommitteeResponse)
async def get_committee(
    committee_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    result = await db.execute(select(CreditCommittee).where(CreditCommittee.id == committee_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Committee not found")
    return item


@router.post("/", response_model=CreditCommitteeResponse, status_code=status.HTTP_201_CREATED)
async def create_committee(
    committee_data: CreditCommitteeCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:create"))
):
    item = CreditCommittee(
        company_id=committee_data.company_id,
        name=committee_data.name,
        description=committee_data.description,
        meeting_date=committee_data.meeting_date,
        status=committee_data.status
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.put("/{committee_id}", response_model=CreditCommitteeResponse)
async def update_committee(
    committee_id: UUID,
    committee_data: CreditCommitteeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:update"))
):
    result = await db.execute(select(CreditCommittee).where(CreditCommittee.id == committee_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Committee not found")

    update_data = committee_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    await db.flush()
    await db.refresh(item)
    return item


@router.delete("/{committee_id}")
async def delete_committee(
    committee_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:delete"))
):
    result = await db.execute(select(CreditCommittee).where(CreditCommittee.id == committee_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Committee not found")

    item.is_active = False
    await db.flush()
    return {"message": "Committee deleted successfully"}


@router.get("/{committee_id}/members", response_model=List[CommitteeMemberResponse])
async def list_committee_members(
    committee_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    result = await db.execute(
        select(CommitteeMember)
        .where(CommitteeMember.committee_id == committee_id)
        .where(CommitteeMember.is_active == True)
    )
    return result.scalars().all()


@router.post("/{committee_id}/members", response_model=CommitteeMemberResponse, status_code=status.HTTP_201_CREATED)
async def add_committee_member(
    committee_id: UUID,
    member_data: CommitteeMemberCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:create"))
):
    result = await db.execute(select(CreditCommittee).where(CreditCommittee.id == committee_id))
    committee = result.scalar_one_or_none()
    if not committee:
        raise HTTPException(status_code=404, detail="Committee not found")

    existing = await db.execute(
        select(CommitteeMember).where(
            CommitteeMember.committee_id == committee_id,
            CommitteeMember.user_id == member_data.user_id
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Member already exists in this committee")

    member = CommitteeMember(
        committee_id=committee_id,
        user_id=member_data.user_id,
        role_in_committee=member_data.role_in_committee
    )
    db.add(member)
    await db.flush()
    await db.refresh(member)
    return member


@router.delete("/{committee_id}/members/{user_id}")
async def remove_committee_member(
    committee_id: UUID,
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:delete"))
):
    result = await db.execute(
        select(CommitteeMember).where(
            CommitteeMember.committee_id == committee_id,
            CommitteeMember.user_id == user_id
        )
    )
    member = result.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found in committee")

    member.is_active = False
    await db.flush()
    return {"message": "Member removed from committee"}


@router.get("/{committee_id}/decisions", response_model=List[CommitteeDecisionResponse])
async def list_committee_decisions(
    committee_id: UUID,
    application_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    query = select(CommitteeDecision).where(CommitteeDecision.committee_id == committee_id)
    if application_id:
        query = query.where(CommitteeDecision.application_id == application_id)

    result = await db.execute(query.order_by(CommitteeDecision.vote_date.desc()))
    return result.scalars().all()


@router.post("/{committee_id}/vote", response_model=CommitteeDecisionResponse, status_code=status.HTTP_201_CREATED)
async def vote_on_application(
    committee_id: UUID,
    application_id: UUID,
    vote: str,
    decision: str,
    comments: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:approve"))
):
    result = await db.execute(select(CreditCommittee).where(CreditCommittee.id == committee_id))
    committee = result.scalar_one_or_none()
    if not committee:
        raise HTTPException(status_code=404, detail="Committee not found")

    member_check = await db.execute(
        select(CommitteeMember).where(
            CommitteeMember.committee_id == committee_id,
            CommitteeMember.user_id == current_user.id,
            CommitteeMember.is_active == True
        )
    )
    if not member_check.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="You are not a member of this committee")

    existing_vote = await db.execute(
        select(CommitteeDecision).where(
            CommitteeDecision.committee_id == committee_id,
            CommitteeDecision.application_id == application_id,
            CommitteeDecision.voted_by == current_user.id
        )
    )
    if existing_vote.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="You have already voted on this application")

    valid_votes = ["approve", "reject", "abstain"]
    if vote.lower() not in valid_votes:
        raise HTTPException(status_code=400, detail=f"Invalid vote. Valid options: {valid_votes}")

    decision_record = CommitteeDecision(
        committee_id=committee_id,
        application_id=application_id,
        decision=decision,
        vote=vote.lower(),
        voted_by=current_user.id,
        comments=comments
    )
    db.add(decision_record)
    await db.flush()
    await db.refresh(decision_record)
    return decision_record


@router.get("/decisions/{decision_id}", response_model=CommitteeDecisionResponse)
async def get_decision(
    decision_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("credit:read"))
):
    result = await db.execute(select(CommitteeDecision).where(CommitteeDecision.id == decision_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Decision not found")
    return item
