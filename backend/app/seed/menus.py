from typing import List, Dict, Any

MENU_ITEMS: List[Dict[str, Any]] = [
    {"name": "Dashboard", "name_ar": "لوحة التحكم", "icon": "dashboard", "url": "/dashboard", "sort_order": "1", "is_visible": True, "module": "dashboard"},
    {"name": "Customers", "name_ar": "العملاء", "icon": "people", "url": "/customers", "sort_order": "2", "is_visible": True, "module": "customers"},
    {"name": "Credit", "name_ar": "الائتمان", "icon": "credit_card", "url": "/credit", "sort_order": "3", "is_visible": True, "module": "credit"},
    {"name": "Collections", "name_ar": "التحصيل", "icon": "payments", "url": "/collections", "sort_order": "4", "is_visible": True, "module": "collections"},
    {"name": "Legal", "name_ar": "القانوني", "icon": "gavel", "url": "/legal", "sort_order": "5", "is_visible": True, "module": "legal"},
    {"name": "Compliance", "name_ar": "الامتثال", "icon": "verified_user", "url": "/compliance", "sort_order": "6", "is_visible": True, "module": "compliance"},
    {"name": "Reports", "name_ar": "التقارير", "icon": "assessment", "url": "/reports", "sort_order": "7", "is_visible": True, "module": "reports"},
    {"name": "Documents", "name_ar": "الوثائق", "icon": "folder", "url": "/documents", "sort_order": "8", "is_visible": True, "module": "documents"},
    {"name": "Settings", "name_ar": "الإعدادات", "icon": "settings", "url": "/settings", "sort_order": "9", "is_visible": True, "module": "settings"},
    {"name": "Users", "name_ar": "المستخدمين", "icon": "group", "url": "/users", "sort_order": "10", "is_visible": True, "module": "users"},
]
