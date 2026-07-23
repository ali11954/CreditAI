from app.celery_app import celery_app
from uuid import UUID


@celery_app.task(bind=True)
def analyze_customer_task(self, customer_id: str, analysis_type: str = "comprehensive"):
    return {
        "customer_id": customer_id,
        "analysis_type": analysis_type,
        "status": "completed"
    }


@celery_app.task(bind=True)
def calculate_credit_score_task(self, customer_id: str):
    return {
        "customer_id": customer_id,
        "score": 720,
        "status": "completed"
    }


@celery_app.task(bind=True)
def run_aml_check_task(self, customer_id: str):
    return {
        "customer_id": customer_id,
        "result": "clear",
        "status": "completed"
    }
