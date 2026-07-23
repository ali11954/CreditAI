from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, and_, extract
from typing import Optional, List
from uuid import UUID
from datetime import datetime, timedelta

from app.database import get_db
from app.services.report_service import ReportService
from app.schemas.report import ReportTemplateCreate, ReportTemplateResponse
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user, require_permission
from app.models.sales import SalesInvoice
from app.models.customer import Customer
from app.models.core import Currency

router = APIRouter()


@router.get("/templates", response_model=PaginatedResponse[ReportTemplateResponse])
async def list_templates(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    module: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("reports:read"))
):
    report_service = ReportService(db)
    templates, total = await report_service.get_templates(
        page=page,
        page_size=page_size,
        module=module
    )
    return PaginatedResponse(
        items=templates,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


@router.get("/templates/{template_id}", response_model=ReportTemplateResponse)
async def get_template(
    template_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("reports:read"))
):
    report_service = ReportService(db)
    template = await report_service.get_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.post("/templates", response_model=ReportTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    template_data: ReportTemplateCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("reports:create"))
):
    report_service = ReportService(db)
    template = await report_service.create_template(template_data)
    return template


@router.post("/execute/{template_id}")
async def execute_report(
    template_id: UUID,
    parameters: dict = {},
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("reports:execute"))
):
    report_service = ReportService(db)
    execution = await report_service.execute_report(template_id, parameters, current_user.id)
    return execution


@router.get("/executions")
async def list_executions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    template_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("reports:read"))
):
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/aging")
async def aging_report(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("reports:read"))
):
    now = datetime.utcnow()
    query = (
        select(
            SalesInvoice.id,
            SalesInvoice.invoice_number,
            SalesInvoice.customer_id,
            Customer.name.label("customer_name"),
            Customer.name_ar.label("customer_name_ar"),
            SalesInvoice.total_amount,
            SalesInvoice.paid_amount,
            SalesInvoice.balance,
            SalesInvoice.due_date,
            SalesInvoice.status,
            Currency.code.label("currency_code"),
            func.extract('day', func.age(now, SalesInvoice.due_date)).label("days_overdue"),
        )
        .outerjoin(Customer, SalesInvoice.customer_id == Customer.id)
        .outerjoin(Currency, SalesInvoice.currency_id == Currency.id)
        .where(SalesInvoice.is_active == True)
        .where(SalesInvoice.balance > 0)
        .order_by(func.extract('day', func.age(now, SalesInvoice.due_date)).desc())
    )
    result = await db.execute(query)
    rows = result.all()

    aging_buckets = {
        "current": {"label": "الحالية (لم تتأخر)", "count": 0, "total": 0.0, "items": []},
        "1_30": {"label": "1-30 يوم", "count": 0, "total": 0.0, "items": []},
        "31_60": {"label": "31-60 يوم", "count": 0, "total": 0.0, "items": []},
        "61_90": {"label": "61-90 يوم", "count": 0, "total": 0.0, "items": []},
        "90_plus": {"label": "أكثر من 90 يوم", "count": 0, "total": 0.0, "items": []},
    }

    for row in rows:
        days = row[10] or 0
        if days < 0:
            bucket = "current"
        elif days <= 30:
            bucket = "1_30"
        elif days <= 60:
            bucket = "31_60"
        elif days <= 90:
            bucket = "61_90"
        else:
            bucket = "90_plus"

        balance = float(row[7] or 0)
        aging_buckets[bucket]["count"] += 1
        aging_buckets[bucket]["total"] += balance
        aging_buckets[bucket]["items"].append({
            "id": row[0],
            "invoice_number": row[1],
            "customer_name": row[4] or row[3],
            "total_amount": float(row[5] or 0),
            "paid_amount": float(row[6] or 0),
            "balance": balance,
            "due_date": row[8].isoformat() if row[8] else None,
            "days_overdue": int(days),
            "currency_code": row[9] or "YER_N",
        })

    total_overdue = sum(b["total"] for b in aging_buckets.values())
    total_count = sum(b["count"] for b in aging_buckets.values())

    return {
        "summary": {
            "total_overdue_amount": total_overdue,
            "total_overdue_invoices": total_count,
            "generated_at": now.isoformat(),
        },
        "buckets": {k: {"label": v["label"], "count": v["count"], "total": v["total"], "items": v["items"]} for k, v in aging_buckets.items()},
    }


@router.get("/sales-summary")
async def sales_summary(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("reports:read"))
):
    now = datetime.utcnow()
    thirty_days_ago = now - timedelta(days=30)
    sixty_days_ago = now - timedelta(days=60)
    ninety_days_ago = now - timedelta(days=90)

    base = select(SalesInvoice).where(SalesInvoice.is_active == True)

    total_result = await db.execute(
        select(
            func.count(SalesInvoice.id),
            func.coalesce(func.sum(SalesInvoice.total_amount), 0),
            func.coalesce(func.sum(SalesInvoice.paid_amount), 0),
            func.coalesce(func.sum(SalesInvoice.balance), 0),
        ).where(SalesInvoice.is_active == True)
    )
    total_row = total_result.first()

    last_30_result = await db.execute(
        select(
            func.count(SalesInvoice.id),
            func.coalesce(func.sum(SalesInvoice.total_amount), 0),
        ).where(
            SalesInvoice.is_active == True,
            SalesInvoice.created_at >= thirty_days_ago
        )
    )
    last_30_row = last_30_result.first()

    status_result = await db.execute(
        select(
            SalesInvoice.status,
            func.count(SalesInvoice.id),
            func.coalesce(func.sum(SalesInvoice.balance), 0),
        )
        .where(SalesInvoice.is_active == True)
        .group_by(SalesInvoice.status)
    )
    status_rows = status_result.all()

    overdue_result = await db.execute(
        select(
            func.count(SalesInvoice.id),
            func.coalesce(func.sum(SalesInvoice.balance), 0),
        ).where(
            SalesInvoice.is_active == True,
            SalesInvoice.due_date < now,
            SalesInvoice.balance > 0
        )
    )
    overdue_row = overdue_result.first()

    top_customers_result = await db.execute(
        select(
            Customer.name,
            Customer.name_ar,
            func.count(SalesInvoice.id).label("invoice_count"),
            func.coalesce(func.sum(SalesInvoice.total_amount), 0).label("total_amount"),
            func.coalesce(func.sum(SalesInvoice.balance), 0).label("balance"),
        )
        .outerjoin(Customer, SalesInvoice.customer_id == Customer.id)
        .where(SalesInvoice.is_active == True)
        .group_by(Customer.id, Customer.name, Customer.name_ar)
        .order_by(func.sum(SalesInvoice.total_amount).desc())
        .limit(10)
    )
    top_customers = top_customers_result.all()

    return {
        "overall": {
            "total_invoices": total_row[0],
            "total_amount": float(total_row[1]),
            "total_paid": float(total_row[2]),
            "total_balance": float(total_row[3]),
        },
        "last_30_days": {
            "invoice_count": last_30_row[0],
            "total_amount": float(last_30_row[1]),
        },
        "by_status": [
            {"status": r[0], "count": r[1], "balance": float(r[2])} for r in status_rows
        ],
        "overdue": {
            "count": overdue_row[0],
            "total_balance": float(overdue_row[1]),
        },
        "top_customers": [
            {
                "name": r[1] or r[0],
                "invoice_count": r[2],
                "total_amount": float(r[3]),
                "balance": float(r[4]),
            }
            for r in top_customers
        ],
        "generated_at": now.isoformat(),
    }


@router.get("/risk-assessment")
async def risk_assessment(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("reports:read"))
):
    now = datetime.utcnow()

    customer_query = (
        select(
            Customer.id,
            Customer.name,
            Customer.name_ar,
            Customer.credit_score,
            Customer.status.label("customer_status"),
            func.count(SalesInvoice.id).label("invoice_count"),
            func.coalesce(func.sum(SalesInvoice.total_amount), 0).label("total_amount"),
            func.coalesce(func.sum(SalesInvoice.paid_amount), 0).label("paid_amount"),
            func.coalesce(func.sum(SalesInvoice.balance), 0).label("balance"),
        )
        .outerjoin(SalesInvoice, and_(
            SalesInvoice.customer_id == Customer.id,
            SalesInvoice.is_active == True
        ))
        .where(Customer.is_active == True)
        .group_by(Customer.id, Customer.name, Customer.name_ar, Customer.credit_score, Customer.status)
    )
    result = await db.execute(customer_query)
    customers = result.all()

    risk_data = []
    for cust in customers:
        total = float(cust[7] or 0)
        paid = float(cust[8] or 0)
        balance = float(cust[9] or 0)
        payment_ratio = (paid / total * 100) if total > 0 else 0

        if balance > 0:
            overdue_result = await db.execute(
                select(func.coalesce(func.sum(SalesInvoice.balance), 0))
                .where(
                    SalesInvoice.customer_id == cust[0],
                    SalesInvoice.is_active == True,
                    SalesInvoice.due_date < now,
                    SalesInvoice.balance > 0
                )
            )
            overdue_balance = float(overdue_result.scalar() or 0)
        else:
            overdue_balance = 0

        if payment_ratio >= 90:
            risk_level = "low"
            risk_score = 90
        elif payment_ratio >= 70:
            risk_level = "medium"
            risk_score = 70
        elif payment_ratio >= 50:
            risk_level = "high"
            risk_score = 40
        else:
            risk_level = "critical"
            risk_score = 20

        risk_data.append({
            "customer_id": cust[0],
            "customer_name": cust[2] or cust[1],
            "credit_score": cust[3],
            "customer_status": cust[4],
            "invoice_count": cust[5],
            "total_amount": total,
            "paid_amount": paid,
            "balance": balance,
            "payment_ratio": round(payment_ratio, 2),
            "overdue_balance": overdue_balance,
            "risk_level": risk_level,
            "risk_score": risk_score,
        })

    risk_data.sort(key=lambda x: x["risk_score"])

    risk_summary = {
        "low": {"count": 0, "total_balance": 0.0},
        "medium": {"count": 0, "total_balance": 0.0},
        "high": {"count": 0, "total_balance": 0.0},
        "critical": {"count": 0, "total_balance": 0.0},
    }
    for item in risk_data:
        risk_summary[item["risk_level"]]["count"] += 1
        risk_summary[item["risk_level"]]["total_balance"] += item["balance"]

    return {
        "summary": risk_summary,
        "customers": risk_data,
        "generated_at": now.isoformat(),
    }
