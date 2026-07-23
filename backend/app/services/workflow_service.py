from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.workflow import WorkflowTemplate, WorkflowInstance, WorkflowStep
from app.schemas.workflow import WorkflowTemplateCreate


class WorkflowService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_templates(
        self,
        page: int = 1,
        page_size: int = 20,
        module: Optional[str] = None
    ) -> Tuple[List[WorkflowTemplate], int]:
        query = select(WorkflowTemplate)
        
        if module:
            query = query.where(WorkflowTemplate.module == module)
        
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        templates = result.scalars().all()
        
        return templates, total
    
    async def get_template(self, template_id: UUID) -> Optional[WorkflowTemplate]:
        result = await self.db.execute(
            select(WorkflowTemplate).where(WorkflowTemplate.id == template_id)
        )
        return result.scalar_one_or_none()
    
    async def create_template(self, data: WorkflowTemplateCreate) -> WorkflowTemplate:
        template = WorkflowTemplate(
            name=data.name,
            description=data.description,
            module=data.module,
            is_active=data.is_active,
            steps=data.steps
        )
        self.db.add(template)
        await self.db.commit()
        await self.db.refresh(template)
        return template
    
    async def get_instances(
        self,
        page: int = 1,
        page_size: int = 20,
        entity_type: Optional[str] = None,
        status: Optional[str] = None
    ) -> Tuple[List[WorkflowInstance], int]:
        query = select(WorkflowInstance)
        
        if entity_type:
            query = query.where(WorkflowInstance.entity_type == entity_type)
        
        if status:
            query = query.where(WorkflowInstance.status == status)
        
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        instances = result.scalars().all()
        
        return instances, total
    
    async def create_instance(
        self,
        template_id: UUID,
        entity_type: str,
        entity_id: UUID,
        user_id: UUID
    ) -> WorkflowInstance:
        instance = WorkflowInstance(
            template_id=template_id,
            entity_type=entity_type,
            entity_id=entity_id,
            initiated_by=user_id
        )
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance
    
    async def approve_step(
        self,
        instance_id: UUID,
        user_id: UUID,
        comments: Optional[str] = None
    ) -> Optional[WorkflowInstance]:
        result = await self.db.execute(
            select(WorkflowInstance).where(WorkflowInstance.id == instance_id)
        )
        instance = result.scalar_one_or_none()
        
        if not instance:
            return None
        
        instance.current_step += 1
        if comments:
            instance.notes = comments
        
        await self.db.commit()
        await self.db.refresh(instance)
        return instance
