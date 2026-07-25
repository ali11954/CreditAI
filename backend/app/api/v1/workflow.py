from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID
from datetime import datetime

from app.database import get_db
from app.services.workflow_service import WorkflowService
from app.schemas.workflow import WorkflowTemplateCreate, WorkflowTemplateResponse
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user, require_permission

router = APIRouter()


@router.get("/templates", response_model=PaginatedResponse[WorkflowTemplateResponse])
async def list_templates(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    module: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("workflow:read"))
):
    workflow_service = WorkflowService(db)
    templates, total = await workflow_service.get_templates(
        page=page,
        page_size=page_size,
        module=module
    )
    return PaginatedResponse(
        items=templates,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


@router.get("/templates/{template_id}", response_model=WorkflowTemplateResponse)
async def get_template(
    template_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("workflow:read"))
):
    workflow_service = WorkflowService(db)
    template = await workflow_service.get_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.post("/templates", response_model=WorkflowTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    template_data: WorkflowTemplateCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("workflow:create"))
):
    workflow_service = WorkflowService(db)
    template = await workflow_service.create_template(template_data)
    return template


@router.get("/instances")
async def list_instances(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    entity_type: Optional[str] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("workflow:read"))
):
    from app.models.workflow import WorkflowInstance, WorkflowTemplate, WorkflowStep
    from sqlalchemy import select, func
    query = select(WorkflowInstance).where(WorkflowInstance.is_active == True)
    count_query = select(func.count(WorkflowInstance.id)).where(WorkflowInstance.is_active == True)
    if entity_type:
        query = query.where(WorkflowInstance.entity_type == entity_type)
        count_query = count_query.where(WorkflowInstance.entity_type == entity_type)
    if status:
        query = query.where(WorkflowInstance.status == status)
        count_query = count_query.where(WorkflowInstance.status == status)
    total = (await db.execute(count_query)).scalar() or 0
    query = query.order_by(WorkflowInstance.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    instances = [dict(row._mapping) for row in result.all()]
    return PaginatedResponse(items=instances, total=total, page=page, page_size=page_size, total_pages=(total + page_size - 1) // page_size)


@router.post("/instances", status_code=status.HTTP_201_CREATED)
async def create_instance(
    instance_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("workflow:create"))
):
    from app.models.workflow import WorkflowInstance, WorkflowTemplate, WorkflowStep
    template = await db.get(WorkflowTemplate, instance_data.get("template_id"))
    if not template:
        raise HTTPException(status_code=404, detail="Workflow template not found")
    instance = WorkflowInstance(
        template_id=instance_data["template_id"],
        entity_type=instance_data["entity_type"],
        entity_id=instance_data["entity_id"],
        initiated_by=current_user.id,
        status="in_progress",
        current_step=1
    )
    db.add(instance)
    await db.flush()
    steps = template.steps or []
    for i, step_def in enumerate(steps):
        step = WorkflowStep(
            instance_id=instance.id,
            step_number=i + 1,
            name=step_def.get("name", f"Step {i+1}"),
            assignee_id=step_def.get("assignee_id"),
            status="pending" if i == 0 else "waiting"
        )
        db.add(step)
    await db.commit()
    await db.refresh(instance)
    return dict(instance._mapping)


@router.post("/instances/{instance_id}/approve")
async def approve_step(
    instance_id: UUID,
    comments: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("workflow:approve"))
):
    from app.models.workflow import WorkflowInstance, WorkflowStep
    from sqlalchemy import select
    instance = await db.get(WorkflowInstance, instance_id)
    if not instance:
        raise HTTPException(status_code=404, detail="Workflow instance not found")
    if instance.status != "in_progress":
        raise HTTPException(status_code=400, detail="Workflow is not in progress")
    result = await db.execute(
        select(WorkflowStep)
        .where(WorkflowStep.instance_id == instance_id)
        .where(WorkflowStep.step_number == instance.current_step)
        .where(WorkflowStep.is_active == True)
    )
    current_step = result.scalar_one_or_none()
    if not current_step:
        raise HTTPException(status_code=404, detail="Current step not found")
    current_step.status = "approved"
    current_step.action = "approved"
    current_step.comments = comments
    current_step.completed_at = datetime.utcnow()
    from sqlalchemy import func
    max_step_result = await db.execute(
        select(func.max(WorkflowStep.step_number))
        .where(WorkflowStep.instance_id == instance_id)
        .where(WorkflowStep.is_active == True)
    )
    max_step = max_step_result.scalar() or 1
    if instance.current_step >= max_step:
        instance.status = "completed"
        instance.completed_at = datetime.utcnow()
    else:
        instance.current_step += 1
        next_result = await db.execute(
            select(WorkflowStep)
            .where(WorkflowStep.instance_id == instance_id)
            .where(WorkflowStep.step_number == instance.current_step)
            .where(WorkflowStep.is_active == True)
        )
        next_step = next_result.scalar_one_or_none()
        if next_step:
            next_step.status = "pending"
    await db.commit()
    return {"message": "Step approved successfully", "status": instance.status}


@router.post("/instances/{instance_id}/reject")
async def reject_step(
    instance_id: UUID,
    reason: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("workflow:approve"))
):
    from app.models.workflow import WorkflowInstance, WorkflowStep
    from sqlalchemy import select
    instance = await db.get(WorkflowInstance, instance_id)
    if not instance:
        raise HTTPException(status_code=404, detail="Workflow instance not found")
    if instance.status != "in_progress":
        raise HTTPException(status_code=400, detail="Workflow is not in progress")
    result = await db.execute(
        select(WorkflowStep)
        .where(WorkflowStep.instance_id == instance_id)
        .where(WorkflowStep.step_number == instance.current_step)
        .where(WorkflowStep.is_active == True)
    )
    current_step = result.scalar_one_or_none()
    if not current_step:
        raise HTTPException(status_code=404, detail="Current step not found")
    current_step.status = "rejected"
    current_step.action = "rejected"
    current_step.comments = reason
    current_step.completed_at = datetime.utcnow()
    instance.status = "rejected"
    await db.commit()
    return {"message": "Step rejected", "status": "rejected"}
