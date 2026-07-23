import re
from typing import Optional


def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    pattern = r'^\+?[1-9]\d{1,14}$'
    return bool(re.match(pattern, phone.replace(" ", "").replace("-", "")))


def validate_national_id(national_id: str) -> bool:
    return len(national_id) >= 10 and national_id.isdigit()


def validate_commercial_register(cr: str) -> bool:
    return len(cr) >= 5 and cr.isdigit()


def validate_vat_number(vat: str) -> bool:
    return len(vat) >= 10 and vat.isdigit()


def validate_iban(iban: str) -> bool:
    cleaned = iban.replace(" ", "")
    return len(cleaned) >= 15 and cleaned[:2].isalpha()


def validate_swift_code(swift: str) -> bool:
    return len(swift) == 8 or len(swift) == 11


def validate_password(password: str) -> tuple[bool, Optional[str]]:
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    return True, None


def validate_amount(amount: str) -> bool:
    try:
        float(amount)
        return True
    except ValueError:
        return False
