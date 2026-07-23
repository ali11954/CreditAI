from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime

from app.models.report import ReportTemplate, ReportExecution
from app.schemas.report import ReportTemplateCreate


class ReportService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_templates(
        self,
        page: int = 1,
        page_size: int = 20,
        module: Optional[str] = None
    ) -> Tuple[List[ReportTemplate], int]:
        query = select(ReportTemplate)
        
        if module:
            query = query.where(ReportTemplate.module == module)
        
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        templates = result.scalars().all()
        
        return templates, total
    
    async def get_template(self, template_id: UUID) -> Optional[ReportTemplate]:
        result = await self.db.execute(
            select(ReportTemplate).where(ReportTemplate.id == template_id)
        )
        return result.scalar_one_or_none()
    
    async def create_template(self, data: ReportTemplateCreate) -> ReportTemplate:
        template = ReportTemplate(
            name=data.name,
            name_ar=data.name_ar,
            description=data.description,
            module=data.module,
            query_template=data.query_template,
            parameters=data.parameters,
            format=data.format,
            is_active=data.is_active,
            company_id=data.company_id
        )
        self.db.add(template)
        await self.db.commit()
        await self.db.refresh(template)
        return template
    
    async def execute_report(
        self,
        template_id: UUID,
        parameters: dict,
        user_id: UUID
    ) -> ReportExecution:
        execution = ReportExecution(
            template_id=template_id,
            executed_by=user_id,
            parameters=parameters,
            status="pending"
        )
        self.db.add(execution)
        await self.db.commit()
        await self.db.refresh(execution)
        return execution
    
    async def get_executions(
        self,
        page: int = 1,
        page_size: int = 20,
        template_id: Optional[UUID] = None
    ) -> Tuple[List[ReportExecution], int]:
        query = select(ReportExecution)
        
        if template_id:
            query = query.where(ReportExecution.template_id == template_id)
        
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        executions = result.scalars().all()
        
        return executions, total
