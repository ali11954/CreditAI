from typing import List, Dict, Any

DEFAULT_ADMIN_USER = {
    "email": "admin@creditai.com",
    "username": "admin",
    "full_name": "System Administrator",
    "full_name_ar": "مسؤول النظام",
    "phone": "+972-50-000-0000",
    "password": "Admin@123",
    "is_superuser": True,
    "is_active": True,
    "roles": ["Super Admin"]
}

DEFAULT_USERS: List[Dict[str, Any]] = [
    DEFAULT_ADMIN_USER,
    {
        "email": "credit.manager@creditai.com",
        "username": "credit.manager",
        "full_name": "Credit Manager",
        "full_name_ar": "مدير الائتمان",
        "phone": "+972-50-111-1111",
        "password": "CreditMgr@123",
        "is_superuser": False,
        "is_active": True,
        "roles": ["Credit Manager"]
    },
    {
        "email": "analyst@creditai.com",
        "username": "analyst",
        "full_name": "Credit Analyst",
        "full_name_ar": "محلل ائتماني",
        "phone": "+972-50-222-2222",
        "password": "Analyst@123",
        "is_superuser": False,
        "is_active": True,
        "roles": ["Credit Analyst"]
    },
    {
        "email": "collection@creditai.com",
        "username": "collection",
        "full_name": "Collection Manager",
        "full_name_ar": "مدير التحصيل",
        "phone": "+972-50-333-3333",
        "password": "Collection@123",
        "is_superuser": False,
        "is_active": True,
        "roles": ["Collection Manager"]
    },
    {
        "email": "legal@creditai.com",
        "username": "legal",
        "full_name": "Legal Manager",
        "full_name_ar": "مدير الشؤون القانونية",
        "phone": "+972-50-444-4444",
        "password": "Legal@123",
        "is_superuser": False,
        "is_active": True,
        "roles": ["Legal Manager"]
    },
    {
        "email": "compliance@creditai.com",
        "username": "compliance",
        "full_name": "Compliance Manager",
        "full_name_ar": "مدير الامتثال",
        "phone": "+972-50-555-5555",
        "password": "Compliance@123",
        "is_superuser": False,
        "is_active": True,
        "roles": ["Compliance Manager"]
    }
]
