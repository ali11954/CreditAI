from app.celery_app import celery_app
import httpx
from app.config import settings


@celery_app.task(bind=True, max_retries=3)
def send_sms_task(self, phone: str, message: str):
    try:
        if settings.SMS_API_URL and settings.SMS_API_KEY:
            with httpx.Client() as client:
                response = client.post(
                    settings.SMS_API_URL,
                    json={
                        "phone": phone,
                        "message": message
                    },
                    headers={"Authorization": f"Bearer {settings.SMS_API_KEY}"}
                )
                return {"status": "sent", "phone": phone, "response": response.status_code}
        
        return {"status": "skipped", "phone": phone, "reason": "SMS not configured"}
    except Exception as exc:
        self.retry(exc=exc, countdown=60)
