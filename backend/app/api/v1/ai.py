from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from app.database import get_db
from app.models.customer import Customer
from app.models.sales import SalesInvoice
from app.models.credit import CreditApplication
from app.services.ai_service import AIService
from app.dependencies import get_current_active_user, require_permission


class CustomerAnalysisRequest(BaseModel):
    customer_id: UUID


router = APIRouter()


@router.post("/analyze-customer")
async def analyze_customer(
    req: CustomerAnalysisRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("ai:use"))
):
    ai_service = AIService(db)
    result = await ai_service.analyze_customer(req.customer_id, "comprehensive", current_user.id)
    return result


@router.post("/credit-score")
async def calculate_credit_score(
    req: CustomerAnalysisRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("ai:use"))
):
    ai_service = AIService(db)
    result = await ai_service.calculate_credit_score(req.customer_id, current_user.id)
    return result


@router.post("/risk-assessment")
async def assess_risk(
    req: CustomerAnalysisRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("ai:use"))
):
    ai_service = AIService(db)
    result = await ai_service.assess_risk_for_customer(req.customer_id, current_user.id)
    return result


@router.get("/prompts")
async def list_prompts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    module: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("ai:read"))
):
    from app.models.ai import AIPrompt
    from sqlalchemy import select, func
    query = select(AIPrompt).where(AIPrompt.is_active == True)
    count_query = select(func.count(AIPrompt.id)).where(AIPrompt.is_active == True)
    if module:
        query = query.where(AIPrompt.module == module)
        count_query = count_query.where(AIPrompt.module == module)
    total = (await db.execute(count_query)).scalar() or 0
    query = query.order_by(AIPrompt.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    prompts = [dict(row._mapping) for row in result.all()]
    return {"items": prompts, "total": total, "page": page, "page_size": page_size}


@router.post("/prompts", status_code=status.HTTP_201_CREATED)
async def create_prompt(
    prompt_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("ai:create"))
):
    from app.models.ai import AIPrompt
    prompt = AIPrompt(**prompt_data, created_by=current_user.id)
    db.add(prompt)
    await db.commit()
    await db.refresh(prompt)
    return dict(prompt._mapping)


@router.post("/chat")
async def ai_chat(
    message: str,
    context: Optional[dict] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("ai:use"))
):
    ai_service = AIService(db)
    result = await ai_service.chat(message, context, current_user.id)
    return result
