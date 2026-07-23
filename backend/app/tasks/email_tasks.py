from app.celery_app import celery_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


@celery_app.task(bind=True, max_retries=3)
def send_email_task(self, to: str, subject: str, body: str, html: bool = False):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = "noreply@creditai.com"
        msg["To"] = to
        
        if html:
            msg.attach(MIMEText(body, "html"))
        else:
            msg.attach(MIMEText(body, "plain"))
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("user", "password")
            server.send_message(msg)
        
        return {"status": "sent", "to": to}
    except Exception as exc:
        self.retry(exc=exc, countdown=60)


@celery_app.task(bind=True, max_retries=3)
def send_bulk_email_task(self, recipients: list, subject: str, body: str):
    results = []
    for recipient in recipients:
        result = send_email_task.delay(recipient, subject, body)
        results.append(result.id)
    return {"status": "queued", "task_ids": results}
