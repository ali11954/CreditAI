from fastapi import APIRouter
from app.api.v1 import (
    auth, users, roles, permissions, companies, branches, departments,
    customers, customer_onboarding, compliance, credit_applications,
    credit_analysis, credit_committee, credit_limits, collateral,
    guarantors, insurance, exposure, collections, legal, documents,
    workflow, ai, communications, reports, sap, audit, settings,
    notifications, dashboards, export, upload, currencies, sales, admin
)

api_router = APIRouter()

api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(roles.router, prefix="/roles", tags=["Roles"])
api_router.include_router(permissions.router, prefix="/permissions", tags=["Permissions"])
api_router.include_router(companies.router, prefix="/companies", tags=["Companies"])
api_router.include_router(branches.router, prefix="/branches", tags=["Branches"])
api_router.include_router(departments.router, prefix="/departments", tags=["Departments"])
api_router.include_router(customers.router, prefix="/customers", tags=["Customers"])
api_router.include_router(customer_onboarding.router, prefix="/customers", tags=["Customer Onboarding"])
api_router.include_router(compliance.router, prefix="/compliance", tags=["Compliance"])
api_router.include_router(credit_applications.router, prefix="/credit-applications", tags=["Credit Applications"])
api_router.include_router(credit_analysis.router, prefix="/credit-analysis", tags=["Credit Analysis"])
api_router.include_router(credit_committee.router, prefix="/credit-committee", tags=["Credit Committee"])
api_router.include_router(credit_limits.router, prefix="/credit-limits", tags=["Credit Limits"])
api_router.include_router(collateral.router, prefix="/collateral", tags=["Collateral"])
api_router.include_router(guarantors.router, prefix="/guarantors", tags=["Guarantors"])
api_router.include_router(insurance.router, prefix="/insurance", tags=["Insurance"])
api_router.include_router(exposure.router, prefix="/exposure", tags=["Exposure"])
api_router.include_router(collections.router, prefix="/collections", tags=["Collections"])
api_router.include_router(legal.router, prefix="/legal", tags=["Legal"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
api_router.include_router(workflow.router, prefix="/workflow", tags=["Workflow"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI"])
api_router.include_router(communications.router, prefix="/communications", tags=["Communications"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(sap.router, prefix="/sap", tags=["SAP Integration"])
api_router.include_router(audit.router, prefix="/audit", tags=["Audit"])
api_router.include_router(settings.router, prefix="/settings", tags=["Settings"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(dashboards.router, prefix="/dashboards", tags=["Dashboards"])
api_router.include_router(export.router, prefix="/export", tags=["Export"])
api_router.include_router(upload.router, prefix="/upload", tags=["Upload"])
api_router.include_router(currencies.router, prefix="/currencies", tags=["Currencies"])
api_router.include_router(sales.router, prefix="/sales", tags=["Sales"])
