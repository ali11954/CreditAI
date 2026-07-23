from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

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
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/instances", status_code=status.HTTP_201_CREATED)
async def create_instance(
    instance_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("workflow:create"))
):
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/instances/{instance_id}/approve")
async def approve_step(
    instance_id: UUID,
    comments: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("workflow:approve"))
):
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/instances/{instance_id}/reject")
async def reject_step(
    instance_id: UUID,
    reason: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("workflow:approve"))
):
    raise HTTPException(status_code=501, detail="Not implemented")
