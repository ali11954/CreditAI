from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Optional, List
from uuid import UUID
from datetime import datetime, timedelta
from pydantic import BaseModel

from app.database import get_db
from app.models.report import Dashboard, DashboardWidget
from app.models.customer import Customer
from app.models.sales import SalesInvoice
from app.models.credit import CreditApplication, CreditLimit
from app.models.collection import Invoice as CollectionInvoice
from app.models.user import User
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user, require_permission


class DashboardCreate(BaseModel):
    name: str
    name_ar: Optional[str] = None
    layout: dict = {}
    widgets: list = []
    is_default: bool = False
    company_id: Optional[UUID] = None


class DashboardUpdate(BaseModel):
    name: Optional[str] = None
    name_ar: Optional[str] = None
    layout: Optional[dict] = None
    widgets: Optional[list] = None
    is_default: Optional[bool] = None
    company_id: Optional[UUID] = None
    is_active: Optional[bool] = None


class DashboardResponse(BaseModel):
    id: UUID
    name: str
    name_ar: Optional[str] = None
    layout: dict = {}
    widgets: list = []
    is_default: bool
    company_id: Optional[UUID] = None
    created_by: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WidgetCreate(BaseModel):
    name: str
    widget_type: str
    config: dict = {}
    data_source: Optional[str] = None
    position: dict = {"x": 0, "y": 0}
    size: dict = {"w": 6, "h": 4}


class WidgetUpdate(BaseModel):
    name: Optional[str] = None
    widget_type: Optional[str] = None
    config: Optional[dict] = None
    data_source: Optional[str] = None
    position: Optional[dict] = None
    size: Optional[dict] = None
    is_active: Optional[bool] = None


class WidgetResponse(BaseModel):
    id: UUID
    dashboard_id: UUID
    name: str
    widget_type: str
    config: dict = {}
    data_source: Optional[str] = None
    position: dict = {}
    size: dict = {}
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


router = APIRouter()


@router.get("/recent-activity")
async def recent_activity(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("dashboards:read"))
):
    from app.models.document import Document
    from app.models.legal import LegalCase

    activities = []

    recent_apps = (await db.execute(
        select(CreditApplication)
        .where(CreditApplication.is_active == True)
        .order_by(CreditApplication.created_at.desc())
        .limit(5)
    )).scalars().all()

    for app in recent_apps:
        customer = (await db.execute(
            select(Customer).where(Customer.id == app.customer_id)
        )).scalar_one_or_none()
        status_map = {
            'draft': ('أنشأ طلب ائتمان', 'warning'),
            'submitted': ('أرسل طلب ائتمان', 'info'),
            'approved': ('وافق على طلب ائتمان', 'success'),
            'rejected': ('رفض طلب ائتمان', 'destructive'),
        }
        action, badge_type = status_map.get(app.status, ('تحديث طلب ائتمان', 'secondary'))
        activities.append({
            "id": str(app.id),
            "user_name": "النظام",
            "action": action,
            "entity": customer.name if customer else "عميل",
            "entity_type": badge_type,
            "time": app.created_at.strftime("%Y-%m-%d %H:%M") if app.created_at else "",
            "type": "info",
        })

    recent_customers = (await db.execute(
        select(Customer)
        .where(Customer.is_active == True)
        .order_by(Customer.created_at.desc())
        .limit(3)
    )).scalars().all()

    for cust in recent_customers:
        activities.append({
            "id": str(cust.id),
            "user_name": "النظام",
            "action": "أضاف عميل جديد",
            "entity": cust.name or cust.name_ar or "عميل",
            "entity_type": "success",
            "time": cust.created_at.strftime("%Y-%m-%d %H:%M") if cust.created_at else "",
            "type": "info",
        })

    recent_sales = (await db.execute(
        select(SalesInvoice)
        .where(SalesInvoice.is_active == True)
        .order_by(SalesInvoice.created_at.desc())
        .limit(3)
    )).scalars().all()

    for inv in recent_sales:
        activities.append({
            "id": str(inv.id),
            "user_name": "النظام",
            "action": "فاتورة مبيعات جديدة",
            "entity": inv.invoice_number or "فاتورة",
            "entity_type": "secondary",
            "time": inv.created_at.strftime("%Y-%m-%d %H:%M") if inv.created_at else "",
            "type": "info",
        })

    activities.sort(key=lambda x: x.get("time", ""), reverse=True)
    return activities[:10]


@router.get("/alerts")
async def dashboard_alerts(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("dashboards:read"))
):
    now = datetime.utcnow()
    alerts = []

    pending_apps = (await db.execute(
        select(func.count()).select_from(CreditApplication).where(
            CreditApplication.is_active == True,
            CreditApplication.status.in_(["draft", "submitted", "pending"])
        )
    )).scalar() or 0

    if pending_apps > 0:
        alerts.append({
            "id": "pending-apps",
            "title": "طلبات ائتمان تنتظر المراجعة",
            "description": f"{pending_apps} طلب(ات) تحتاج مراجعة",
            "type": "warning",
        })

    overdue = (await db.execute(
        select(func.count()).select_from(SalesInvoice).where(
            SalesInvoice.is_active == True,
            SalesInvoice.due_date < now,
            SalesInvoice.balance > 0
        )
    )).scalar() or 0

    if overdue > 0:
        alerts.append({
            "id": "overdue-invoices",
            "title": "فواتير متأخرة",
            "description": f"{overdue} فاتورة(ات) تجاوزت موعد الدفع",
            "type": "destructive",
        })

    total_customers = (await db.execute(
        select(func.count()).select_from(Customer).where(Customer.is_active == True)
    )).scalar() or 0

    if total_customers == 0:
        alerts.append({
            "id": "no-customers",
            "title": "لا يوجد عملاء",
            "description": "لم يتم إضافة أي عميل بعد",
            "type": "info",
        })

    return alerts


@router.get("/summary")
async def dashboard_summary(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("dashboards:read"))
):
    now = datetime.utcnow()
    thirty_days_ago = now - timedelta(days=30)
    sixty_days_ago = now - timedelta(days=60)

    customers_total = (await db.execute(
        select(func.count()).select_from(Customer).where(Customer.is_active == True)
    )).scalar() or 0

    customers_prev = (await db.execute(
        select(func.count()).select_from(Customer).where(
            Customer.is_active == True, Customer.created_at >= sixty_days_ago, Customer.created_at < thirty_days_ago
        )
    )).scalar() or 0

    customers_new = (await db.execute(
        select(func.count()).select_from(Customer).where(
            Customer.is_active == True, Customer.created_at >= thirty_days_ago
        )
    )).scalar() or 0

    apps_total = (await db.execute(
        select(func.count()).select_from(CreditApplication).where(CreditApplication.is_active == True)
    )).scalar() or 0

    apps_prev = (await db.execute(
        select(func.count()).select_from(CreditApplication).where(
            CreditApplication.is_active == True,
            CreditApplication.created_at >= sixty_days_ago,
            CreditApplication.created_at < thirty_days_ago
        )
    )).scalar() or 0

    apps_new = (await db.execute(
        select(func.count()).select_from(CreditApplication).where(
            CreditApplication.is_active == True, CreditApplication.created_at >= thirty_days_ago
        )
    )).scalar() or 0

    exposure_result = await db.execute(
        select(
            func.coalesce(func.sum(SalesInvoice.balance), 0),
        ).where(SalesInvoice.is_active == True)
    )
    total_exposure = float(exposure_result.scalar() or 0)

    exposure_prev_result = await db.execute(
        select(func.coalesce(func.sum(SalesInvoice.balance), 0)).where(
            SalesInvoice.is_active == True,
            SalesInvoice.created_at >= sixty_days_ago,
            SalesInvoice.created_at < thirty_days_ago
        )
    )
    exposure_prev = float(exposure_prev_result.scalar() or 0)

    approved = (await db.execute(
        select(func.count()).select_from(CreditApplication).where(
            CreditApplication.is_active == True, CreditApplication.status == "approved"
        )
    )).scalar() or 0

    approval_rate = round((approved / apps_total * 100), 1) if apps_total > 0 else 0

    approval_prev = (await db.execute(
        select(func.count()).select_from(CreditApplication).where(
            CreditApplication.is_active == True,
            CreditApplication.status == "approved",
            CreditApplication.created_at >= sixty_days_ago,
            CreditApplication.created_at < thirty_days_ago
        )
    )).scalar() or 0
    apps_prev_count = apps_prev if apps_prev > 0 else 1
    approval_rate_prev = round((approval_prev / apps_prev_count * 100), 1) if apps_prev_count > 0 else 0

    overdue_result = await db.execute(
        select(func.count()).select_from(SalesInvoice).where(
            SalesInvoice.is_active == True,
            SalesInvoice.due_date < now,
            SalesInvoice.balance > 0
        )
    )
    overdue_count = overdue_result.scalar() or 0

    pending_apps = (await db.execute(
        select(func.count()).select_from(CreditApplication).where(
            CreditApplication.is_active == True,
            CreditApplication.status.in_(["draft", "submitted", "pending"])
        )
    )).scalar() or 0

    def calc_change(current: float, previous: float) -> dict:
        if previous == 0:
            pct = 100.0 if current > 0 else 0.0
        else:
            pct = round(((current - previous) / previous) * 100, 1)
        return {
            "value": f"+{pct}%" if pct >= 0 else f"{pct}%",
            "type": "positive" if pct >= 0 else "negative"
        }

    customer_change = calc_change(customers_new, customers_prev)
    apps_change = calc_change(apps_new, apps_prev)

    return {
        "stats": {
            "customers": {
                "value": customers_total,
                "change": customer_change["value"],
                "changeType": customer_change["type"],
            },
            "credit_applications": {
                "value": apps_total,
                "change": apps_change["value"],
                "changeType": apps_change["type"],
            },
            "exposure": {
                "value": total_exposure,
                "change": "+0%",
                "changeType": "positive",
            },
            "approval_rate": {
                "value": approval_rate,
                "change": f"{round(approval_rate - approval_rate_prev, 1)}%",
                "changeType": "positive" if approval_rate >= approval_rate_prev else "negative",
            },
            "overdue": {
                "value": overdue_count,
                "changeType": "negative" if overdue_count > 0 else "positive",
            },
            "pending": {
                "value": pending_apps,
                "changeType": "positive" if pending_apps > 0 else "positive",
            },
        },
        "generated_at": now.isoformat(),
    }


@router.get("/data/{widget_type}")
async def get_widget_data(
    widget_type: str,
    params: dict = {},
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("dashboards:read"))
):
    return {
        "widget_type": widget_type,
        "data": {},
        "message": f"Data for widget type '{widget_type}'"
    }


@router.get("/", response_model=PaginatedResponse[DashboardResponse])
async def list_dashboards(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    company_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("dashboards:read"))
):
    query = select(Dashboard)
    if company_id:
        query = query.where(Dashboard.company_id == company_id)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    items = result.scalars().all()

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


@router.get("/{dashboard_id}", response_model=DashboardResponse)
async def get_dashboard(
    dashboard_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("dashboards:read"))
):
    result = await db.execute(select(Dashboard).where(Dashboard.id == dashboard_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return item


@router.post("/", response_model=DashboardResponse, status_code=status.HTTP_201_CREATED)
async def create_dashboard(
    dashboard_data: DashboardCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("dashboards:create"))
):
    item = Dashboard(
        name=dashboard_data.name,
        name_ar=dashboard_data.name_ar,
        layout=dashboard_data.layout,
        widgets=dashboard_data.widgets,
        is_default=dashboard_data.is_default,
        company_id=dashboard_data.company_id,
        created_by=current_user.id
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.put("/{dashboard_id}", response_model=DashboardResponse)
async def update_dashboard(
    dashboard_id: UUID,
    dashboard_data: DashboardUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("dashboards:update"))
):
    result = await db.execute(select(Dashboard).where(Dashboard.id == dashboard_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Dashboard not found")

    update_data = dashboard_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    await db.flush()
    await db.refresh(item)
    return item


@router.delete("/{dashboard_id}")
async def delete_dashboard(
    dashboard_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("dashboards:delete"))
):
    result = await db.execute(select(Dashboard).where(Dashboard.id == dashboard_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Dashboard not found")

    item.is_active = False
    await db.flush()
    return {"message": "Dashboard deleted successfully"}


@router.get("/{dashboard_id}/widgets", response_model=List[WidgetResponse])
async def list_widgets(
    dashboard_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("dashboards:read"))
):
    result = await db.execute(
        select(DashboardWidget)
        .where(DashboardWidget.dashboard_id == dashboard_id)
        .where(DashboardWidget.is_active == True)
    )
    return result.scalars().all()


@router.post("/{dashboard_id}/widgets", response_model=WidgetResponse, status_code=status.HTTP_201_CREATED)
async def add_widget(
    dashboard_id: UUID,
    widget_data: WidgetCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("dashboards:create"))
):
    result = await db.execute(select(Dashboard).where(Dashboard.id == dashboard_id))
    dashboard = result.scalar_one_or_none()
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")

    widget = DashboardWidget(
        dashboard_id=dashboard_id,
        name=widget_data.name,
        widget_type=widget_data.widget_type,
        config=widget_data.config,
        data_source=widget_data.data_source,
        position=widget_data.position,
        size=widget_data.size
    )
    db.add(widget)
    await db.flush()
    await db.refresh(widget)
    return widget


@router.put("/{dashboard_id}/widgets/{widget_id}", response_model=WidgetResponse)
async def update_widget(
    dashboard_id: UUID,
    widget_id: UUID,
    widget_data: WidgetUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("dashboards:update"))
):
    result = await db.execute(
        select(DashboardWidget)
        .where(DashboardWidget.id == widget_id)
        .where(DashboardWidget.dashboard_id == dashboard_id)
    )
    widget = result.scalar_one_or_none()
    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found")

    update_data = widget_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "type":
            setattr(widget, "widget_type", value)
        else:
            setattr(widget, key, value)

    await db.flush()
    await db.refresh(widget)
    return widget


@router.delete("/{dashboard_id}/widgets/{widget_id}")
async def delete_widget(
    dashboard_id: UUID,
    widget_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("dashboards:delete"))
):
    result = await db.execute(
        select(DashboardWidget)
        .where(DashboardWidget.id == widget_id)
        .where(DashboardWidget.dashboard_id == dashboard_id)
    )
    widget = result.scalar_one_or_none()
    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found")

    widget.is_active = False
    await db.flush()
    return {"message": "Widget deleted successfully"}
