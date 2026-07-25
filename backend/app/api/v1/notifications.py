from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

from app.database import get_db
from app.services.notification_service import NotificationService
from app.schemas.notification import NotificationResponse
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[NotificationResponse])
async def list_notifications(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    is_read: Optional[bool] = None,
    type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    notification_service = NotificationService(db)
    notifications, total = await notification_service.get_notifications(
        user_id=current_user.id,
        page=page,
        page_size=page_size,
        is_read=is_read,
        type=type
    )
    return PaginatedResponse(
        items=notifications,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


@router.get("/unread-count")
async def get_unread_count(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    notification_service = NotificationService(db)
    count = await notification_service.get_unread_count(current_user.id)
    return {"count": count}


@router.put("/{notification_id}/read")
async def mark_as_read(
    notification_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    notification_service = NotificationService(db)
    success = await notification_service.mark_as_read(notification_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification marked as read"}


@router.put("/read-all")
async def mark_all_as_read(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    notification_service = NotificationService(db)
    count = await notification_service.mark_all_as_read(current_user.id)
    return {"message": f"Marked {count} notifications as read"}


@router.get("/preferences")
async def get_preferences(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    from app.models.notification import NotificationPreference
    from sqlalchemy import select
    result = await db.execute(
        select(NotificationPreference)
        .where(NotificationPreference.user_id == current_user.id)
        .where(NotificationPreference.is_active == True)
    )
    prefs = [dict(row._mapping) for row in result.all()]
    return {"items": prefs}


@router.put("/preferences")
async def update_preferences(
    preferences: list[dict],
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    from app.models.notification import NotificationPreference
    from sqlalchemy import select
    for pref_data in preferences:
        notif_type = pref_data.get("notification_type")
        channel = pref_data.get("channel")
        is_enabled = pref_data.get("is_enabled", True)
        result = await db.execute(
            select(NotificationPreference)
            .where(NotificationPreference.user_id == current_user.id)
            .where(NotificationPreference.notification_type == notif_type)
            .where(NotificationPreference.channel == channel)
        )
        existing = result.scalar_one_or_none()
        if existing:
            existing.is_enabled = is_enabled
        else:
            pref = NotificationPreference(
                user_id=current_user.id,
                notification_type=notif_type,
                channel=channel,
                is_enabled=is_enabled
            )
            db.add(pref)
    await db.commit()
    return {"message": "Preferences updated successfully"}
