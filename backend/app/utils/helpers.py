from datetime import datetime, date
from typing import Any, Optional
from uuid import UUID
import hashlib
import secrets
import string


def generate_code(length: int = 10) -> str:
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def generate_numeric_code(length: int = 6) -> str:
    return ''.join(secrets.choice(string.digits) for _ in range(length))


def hash_string(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def format_currency(amount: float, currency_code: str = "SAR") -> str:
    return f"{currency_code} {amount:,.2f}"


def calculate_aging_days(due_date: date) -> int:
    today = date.today()
    if due_date < today:
        return (today - due_date).days
    return 0


def serialize_datetime(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    return dt.isoformat()


def deserialize_datetime(dt_str: Optional[str]) -> Optional[datetime]:
    if dt_str is None:
        return None
    return datetime.fromisoformat(dt_str)


def uuid_to_str(uuid_val: Optional[UUID]) -> Optional[str]:
    if uuid_val is None:
        return None
    return str(uuid_val)


def paginate_list(items: list, page: int, page_size: int) -> dict:
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "items": items[start:end],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }
