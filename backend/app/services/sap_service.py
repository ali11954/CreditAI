from typing import Optional, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.sap import SAPSyncQueue, SAPSyncLog


class SAPService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_sync_status(self) -> Dict[str, Any]:
        result = await self.db.execute(
            select(func.count()).select_from(SAPSyncQueue).where(
                SAPSyncQueue.status == "pending"
            )
        )
        pending_count = result.scalar()
        
        return {
            "pending_syncs": pending_count,
            "last_sync": None,
            "status": "connected"
        }
    
    async def sync_entity(
        self,
        entity_type: str,
        entity_id: UUID
    ) -> Dict[str, Any]:
        return {
            "status": "synced",
            "entity_type": entity_type,
            "entity_id": str(entity_id),
            "synced_at": None
        }
    
    async def queue_sync(
        self,
        entity_type: str,
        entity_id: UUID,
        action: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        queue_item = SAPSyncQueue(
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            payload=payload
        )
        self.db.add(queue_item)
        await self.db.commit()
        
        return {
            "id": str(queue_item.id),
            "status": "queued"
        }
