from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from datetime import datetime

from app.models.notification import Notification


class NotificationService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_notifications(
        self,
        user_id: UUID,
        page: int = 1,
        page_size: int = 20,
        is_read: Optional[bool] = None,
        type: Optional[str] = None
    ) -> Tuple[List[Notification], int]:
        query = select(Notification).where(Notification.user_id == user_id)
        
        if is_read is not None:
            query = query.where(Notification.is_read == is_read)
        
        if type:
            query = query.where(Notification.type == type)
        
        query = query.order_by(Notification.created_at.desc())
        
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        notifications = result.scalars().all()
        
        return notifications, total
    
    async def get_unread_count(self, user_id: UUID) -> int:
        result = await self.db.execute(
            select(func.count()).select_from(Notification).where(
                Notification.user_id == user_id,
                Notification.is_read == False
            )
        )
        return result.scalar()
    
    async def mark_as_read(
        self,
        notification_id: UUID,
        user_id: UUID
    ) -> bool:
        result = await self.db.execute(
            select(Notification).where(
                Notification.id == notification_id,
                Notification.user_id == user_id
            )
        )
        notification = result.scalar_one_or_none()
        
        if not notification:
            return False
        
        notification.is_read = True
        notification.read_at = datetime.utcnow()
        await self.db.commit()
        return True
    
    async def mark_all_as_read(self, user_id: UUID) -> int:
        result = await self.db.execute(
            update(Notification)
            .where(
                Notification.user_id == user_id,
                Notification.is_read == False
            )
            .values(is_read=True, read_at=datetime.utcnow())
        )
        await self.db.commit()
        return result.rowcount
    
    async def create_notification(
        self,
        user_id: UUID,
        title: str,
        message: str,
        type: str,
        entity_type: Optional[str] = None,
        entity_id: Optional[UUID] = None,
        action_url: Optional[str] = None
    ) -> Notification:
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=type,
            entity_type=entity_type,
            entity_id=entity_id,
            action_url=action_url
        )
        self.db.add(notification)
        await self.db.commit()
        await self.db.refresh(notification)
        return notification
