from app.celery_app import celery_app
from uuid import UUID


@celery_app.task(bind=True, max_retries=3)
def sync_sap_entity_task(self, entity_type: str, entity_id: str):
    try:
        return {
            "status": "synced",
            "entity_type": entity_type,
            "entity_id": entity_id
        }
    except Exception as exc:
        self.retry(exc=exc, countdown=300)


@celery_app.task(bind=True)
def process_sap_sync_queue_task():
    return {"status": "processed", "count": 0}
