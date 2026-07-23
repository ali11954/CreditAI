from typing import List, Dict, Any

ROLES: List[Dict[str, Any]] = [
    {
        "name": "Super Admin",
        "name_ar": "مسؤول النظام",
        "description": "Full system access",
        "is_system": True,
        "permissions": ["*"]
    },
    {
        "name": "Admin",
        "name_ar": "مدير",
        "description": "Administrative access",
        "is_system": True,
        "permissions": ["users:read", "users:create", "users:update", "users:delete", "roles:read", "roles:create", "roles:update", "roles:delete"]
    },
    {
        "name": "Credit Manager",
        "name_ar": "مدير الائتمان",
        "description": "Credit department manager",
        "is_system": False,
        "permissions": ["credit:read", "credit:create", "credit:update", "credit:approve", "credit:delete"]
    },
    {
        "name": "Credit Analyst",
        "name_ar": "محلل ائتماني",
        "description": "Credit analysis specialist",
        "is_system": False,
        "permissions": ["credit:read", "credit:create", "credit:update"]
    },
    {
        "name": "Collection Manager",
        "name_ar": "مدير التحصيل",
        "description": "Collections department manager",
        "is_system": False,
        "permissions": ["collections:read", "collections:create", "collections:update", "collections:delete"]
    },
    {
        "name": "Collection Officer",
        "name_ar": "مسؤول تحصيل",
        "description": "Collections officer",
        "is_system": False,
        "permissions": ["collections:read", "collections:create", "collections:update"]
    },
    {
        "name": "Legal Manager",
        "name_ar": "مدير الشؤون القانونية",
        "description": "Legal department manager",
        "is_system": False,
        "permissions": ["legal:read", "legal:create", "legal:update", "legal:delete"]
    },
    {
        "name": "Legal Officer",
        "name_ar": "مسؤول قانوني",
        "description": "Legal officer",
        "is_system": False,
        "permissions": ["legal:read", "legal:create", "legal:update"]
    },
    {
        "name": "Compliance Manager",
        "name_ar": "مدير الامتثال",
        "description": "Compliance department manager",
        "is_system": False,
        "permissions": ["compliance:read", "compliance:create", "compliance:update", "compliance:delete"]
    },
    {
        "name": "Compliance Officer",
        "name_ar": "مسؤول امتثال",
        "description": "Compliance officer",
        "is_system": False,
        "permissions": ["compliance:read", "compliance:create", "compliance:update"]
    },
    {
        "name": "Sales Manager",
        "name_ar": "مدير المبيعات",
        "description": "Sales department manager",
        "is_system": False,
        "permissions": ["customers:read", "customers:create", "customers:update"]
    },
    {
        "name": "Salesman",
        "name_ar": "مندوب مبيعات",
        "description": "Sales representative",
        "is_system": False,
        "permissions": ["customers:read", "customers:create"]
    },
    {
        "name": "Finance Manager",
        "name_ar": "مدير المالية",
        "description": "Finance department manager",
        "is_system": False,
        "permissions": ["reports:read", "reports:execute", "finance:read"]
    },
    {
        "name": "Accountant",
        "name_ar": "محاسب",
        "description": "Accounting staff",
        "is_system": False,
        "permissions": ["reports:read", "finance:read"]
    },
    {
        "name": "HR Manager",
        "name_ar": "مدير الموارد البشرية",
        "description": "Human resources manager",
        "is_system": False,
        "permissions": ["users:read", "users:create", "users:update"]
    },
    {
        "name": "IT Admin",
        "name_ar": "مدير تقني",
        "description": "IT administrator",
        "is_system": False,
        "permissions": ["settings:read", "settings:update", "audit:read"]
    },
    {
        "name": "Auditor",
        "name_ar": "مدقق",
        "description": "Internal auditor",
        "is_system": False,
        "permissions": ["audit:read", "reports:read"]
    },
    {
        "name": "Branch Manager",
        "name_ar": "مدير الفرع",
        "description": "Branch manager",
        "is_system": False,
        "permissions": ["customers:read", "credit:read", "collections:read"]
    },
    {
        "name": "Risk Manager",
        "name_ar": "مدير المخاطر",
        "description": "Risk management officer",
        "is_system": False,
        "permissions": ["credit:read", "credit:update", "exposure:read"]
    },
    {
        "name": "Document Controller",
        "name_ar": "مسؤول الوثائق",
        "description": "Document management",
        "is_system": False,
        "permissions": ["documents:read", "documents:create", "documents:update", "documents:delete"]
    },
    {
        "name": "Workflow Admin",
        "name_ar": "مسؤول سير العمل",
        "description": "Workflow management",
        "is_system": False,
        "permissions": ["workflow:read", "workflow:create", "workflow:update"]
    },
    {
        "name": "Report Viewer",
        "name_ar": "مشاهد التقارير",
        "description": "Read-only report access",
        "is_system": False,
        "permissions": ["reports:read"]
    },
    {
        "name": "AI Operator",
        "name_ar": "مشغل الذكاء الاصطناعي",
        "description": "AI tools operator",
        "is_system": False,
        "permissions": ["ai:read", "ai:use"]
    },
    {
        "name": "SAP Operator",
        "name_ar": "مشغل SAP",
        "description": "SAP integration operator",
        "is_system": False,
        "permissions": ["sap:read", "sap:sync"]
    },
    {
        "name": "View Only",
        "name_ar": "عرض فقط",
        "description": "Read-only access to all modules",
        "is_system": False,
        "permissions": ["customers:read", "credit:read", "collections:read", "legal:read", "compliance:read"]
    }
]
