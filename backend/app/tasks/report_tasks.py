from app.celery_app import celery_app
from uuid import UUID


@celery_app.task(bind=True)
def generate_report_task(self, template_id: str, parameters: dict, user_id: str):
    return {
        "template_id": template_id,
        "user_id": user_id,
        "status": "completed",
        "file_path": f"/reports/{template_id}.pdf"
    }


@celery_app.task(bind=True)
def schedule_report_task(self, template_id: str, schedule: str):
    return {
        "template_id": template_id,
        "schedule": schedule,
        "status": "scheduled"
    }
