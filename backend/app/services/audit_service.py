from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime

from app.models.audit import AuditTrail, AIDecisionLog, SecurityEvent


class AuditService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_audit_trail(
        self,
        page: int = 1,
        page_size: int = 20,
        user_id: Optional[UUID] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[UUID] = None
    ) -> Tuple[List[AuditTrail], int]:
        query = select(AuditTrail)
        
        if user_id:
            query = query.where(AuditTrail.user_id == user_id)
        
        if entity_type:
            query = query.where(AuditTrail.entity_type == entity_type)
        
        if entity_id:
            query = query.where(AuditTrail.entity_id == entity_id)
        
        query = query.order_by(AuditTrail.timestamp.desc())
        
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        logs = result.scalars().all()
        
        return logs, total
    
    async def log_action(
        self,
        user_id: Optional[UUID],
        action: str,
        entity_type: str,
        entity_id: Optional[UUID] = None,
        old_values: dict = {},
        new_values: dict = {},
        ip_address: Optional[str] = None
    ) -> AuditTrail:
        log = AuditTrail(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address
        )
        self.db.add(log)
        await self.db.commit()
        await self.db.refresh(log)
        return log
    
    async def get_ai_decisions(
        self,
        page: int = 1,
        page_size: int = 20,
        model_name: Optional[str] = None
    ) -> Tuple[List[AIDecisionLog], int]:
        query = select(AIDecisionLog)
        
        if model_name:
            query = query.where(AIDecisionLog.model_name == model_name)
        
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        logs = result.scalars().all()
        
        return logs, total
    
    async def get_security_events(
        self,
        page: int = 1,
        page_size: int = 20,
        event_type: Optional[str] = None,
        severity: Optional[str] = None
    ) -> Tuple[List[SecurityEvent], int]:
        query = select(SecurityEvent)
        
        if event_type:
            query = query.where(SecurityEvent.event_type == event_type)
        
        if severity:
            query = query.where(SecurityEvent.severity == severity)
        
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        events = result.scalars().all()
        
        return events, total
    
    async def log_security_event(
        self,
        event_type: str,
        user_id: Optional[UUID] = None,
        ip_address: Optional[str] = None,
        details: dict = {},
        severity: str = "info"
    ) -> SecurityEvent:
        event = SecurityEvent(
            event_type=event_type,
            user_id=user_id,
            ip_address=ip_address,
            details=details,
            severity=severity
        )
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event
