from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from uuid import UUID
from datetime import datetime, timedelta
import io

from app.database import get_db
from app.services.collection_service import CollectionService
from app.schemas.collection import (
    InvoiceCreate, InvoiceUpdate, InvoiceResponse,
    CollectionActivityCreate, CollectionActivityResponse,
    PromiseToPayCreate, PromiseToPayResponse,
    InstallmentPlanCreate, InstallmentPlanResponse,
    InstallmentCreate,
    SettlementCreate, SettlementResponse,
    WriteOffCreate, WriteOffResponse,
)
from app.schemas.common import PaginatedResponse, MessageResponse
from app.dependencies import get_current_active_user, require_permission
from app.models.sales import SalesInvoice
from app.models.customer import Customer
from app.models.core import Currency
from app.models.collection import (
    CollectionActivity, PromiseToPay, InstallmentPlan, Installment,
    Settlement, WriteOff,
)

router = APIRouter()


@router.get("/sales-invoices")
async def list_sales_invoices(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    customer_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("collections:read"))
):
    query = (
        select(
            SalesInvoice,
            Customer.name.label("cust_name"),
            Customer.name_ar.label("cust_name_ar"),
            Currency.code.label("currency_code"),
        )
        .outerjoin(Customer, SalesInvoice.customer_id == Customer.id)
        .outerjoin(Currency, SalesInvoice.currency_id == Currency.id)
        .where(SalesInvoice.is_active == True)
    )

    if search:
        query = query.where(SalesInvoice.invoice_number.ilike(f"%{search}%"))
    if status:
        query = query.where(SalesInvoice.status == status)
    if customer_id:
        query = query.where(SalesInvoice.customer_id == customer_id)

    count_query = select(func.count()).select_from(
        select(SalesInvoice.id).where(SalesInvoice.is_active == True).subquery()
    )
    total = (await db.execute(count_query)).scalar()

    query = query.order_by(SalesInvoice.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    rows = result.all()

    enriched = []
    for row in rows:
        inv = row[0]
        cust_name_ar = row[2]
        cust_name = row[1]
        curr_code = row[3] or "YER_N"
        customer_display = cust_name_ar or cust_name

        from datetime import datetime as dt
        now = dt.utcnow()
        due = inv.due_date
        overdue_days = (now - due).days if due and due < now else 0

        enriched.append({
            "id": inv.id,
            "invoice_number": inv.invoice_number,
            "customer_id": inv.customer_id,
            "customer_name": customer_display,
            "invoice_date": inv.invoice_date.isoformat() if inv.invoice_date else None,
            "due_date": inv.due_date.isoformat() if inv.due_date else None,
            "amount": float(inv.amount),
            "tax_amount": float(inv.tax_amount or 0),
            "discount_amount": float(inv.discount_amount or 0),
            "total_amount": float(inv.total_amount),
            "paid_amount": float(inv.paid_amount or 0),
            "balance": float(inv.balance),
            "currency_id": str(inv.currency_id) if inv.currency_id else None,
            "currency_code": curr_code,
            "status": inv.status,
            "overdue_days": overdue_days,
            "product_type": inv.product_type,
            "quantity_tons": float(inv.quantity_tons) if inv.quantity_tons else None,
            "created_at": inv.created_at.isoformat() if inv.created_at else None,
        })

    return PaginatedResponse(
        items=enriched,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


@router.get("/invoices", response_model=PaginatedResponse[InvoiceResponse])
async def list_invoices(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    customer_id: Optional[UUID] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("collections:read"))
):
    collection_service = CollectionService(db)
    invoices, total = await collection_service.get_invoices(
        page=page,
        page_size=page_size,
        customer_id=customer_id,
        status=status
    )
    return PaginatedResponse(
        items=invoices,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


@router.get("/invoices/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(
    invoice_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("collections:read"))
):
    collection_service = CollectionService(db)
    invoice = await collection_service.get_invoice(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.post("/invoices", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
async def create_invoice(
    invoice_data: InvoiceCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("collections:create"))
):
    collection_service = CollectionService(db)
    invoice = await collection_service.create_invoice(invoice_data)
    return invoice


@router.put("/invoices/{invoice_id}", response_model=InvoiceResponse)
async def update_invoice(
    invoice_id: UUID,
    invoice_data: InvoiceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("collections:update"))
):
    collection_service = CollectionService(db)
    invoice = await collection_service.update_invoice(invoice_id, invoice_data)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.delete("/invoices/{invoice_id}")
async def delete_invoice(
    invoice_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("collections:delete"))
):
    collection_service = CollectionService(db)
    success = await collection_service.delete_invoice(invoice_id)
    if not success:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {"message": "Invoice deleted successfully"}


@router.get("/activities", response_model=PaginatedResponse[CollectionActivityResponse])
async def list_activities(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    customer_id: Optional[UUID] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("collections:read"))
):
    query = select(CollectionActivity).where(CollectionActivity.is_active == True)

    if customer_id:
        query = query.where(CollectionActivity.customer_id == customer_id)
    if status:
        query = query.where(CollectionActivity.outcome == status)

    count_query = select(func.count()).select_from(
        select(CollectionActivity.id).where(CollectionActivity.is_active == True).subquery()
    )
    if customer_id:
        count_query = count_query.where(CollectionActivity.customer_id == customer_id)
    if status:
        count_query = count_query.where(CollectionActivity.outcome == status)

    total = (await db.execute(count_query)).scalar()

    query = query.order_by(CollectionActivity.created_at.desc())
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


@router.post("/activities", response_model=CollectionActivityResponse, status_code=status.HTTP_201_CREATED)
async def create_activity(
    activity_data: CollectionActivityCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("collections:create"))
):
    activity = CollectionActivity(
        customer_id=activity_data.customer_id,
        invoice_id=activity_data.invoice_id,
        activity_type=activity_data.activity_type,
        direction=activity_data.direction,
        subject=activity_data.subject,
        content=activity_data.content,
        scheduled_date=activity_data.scheduled_date,
        completed_date=activity_data.completed_date,
        outcome=activity_data.outcome,
        next_action=activity_data.next_action,
        next_action_date=activity_data.next_action_date,
        created_by=current_user.id,
    )
    db.add(activity)
    await db.commit()
    await db.refresh(activity)
    return activity


@router.get("/promises-to-pay", response_model=PaginatedResponse[PromiseToPayResponse])
async def list_promises_to_pay(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    customer_id: Optional[UUID] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("collections:read"))
):
    query = select(PromiseToPay).where(PromiseToPay.is_active == True)

    if customer_id:
        query = query.where(PromiseToPay.customer_id == customer_id)
    if status:
        query = query.where(PromiseToPay.status == status)

    count_query = select(func.count()).select_from(
        select(PromiseToPay.id).where(PromiseToPay.is_active == True).subquery()
    )
    if customer_id:
        count_query = count_query.where(PromiseToPay.customer_id == customer_id)
    if status:
        count_query = count_query.where(PromiseToPay.status == status)

    total = (await db.execute(count_query)).scalar()

    query = query.order_by(PromiseToPay.created_at.desc())
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


@router.post("/promises-to-pay", response_model=PromiseToPayResponse, status_code=status.HTTP_201_CREATED)
async def create_promise_to_pay(
    promise_data: PromiseToPayCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("collections:create"))
):
    promise = PromiseToPay(
        customer_id=promise_data.customer_id,
        promise_date=promise_data.promise_date,
        amount=promise_data.amount,
        status=promise_data.status,
        notes=promise_data.notes,
        created_by=current_user.id,
    )
    db.add(promise)
    await db.commit()
    await db.refresh(promise)
    return promise


@router.get("/installment-plans", response_model=PaginatedResponse[InstallmentPlanResponse])
async def list_installment_plans(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    customer_id: Optional[UUID] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("collections:read"))
):
    query = select(InstallmentPlan).where(InstallmentPlan.is_active == True)

    if customer_id:
        query = query.where(InstallmentPlan.customer_id == customer_id)
    if status:
        query = query.where(InstallmentPlan.status == status)

    count_query = select(func.count()).select_from(
        select(InstallmentPlan.id).where(InstallmentPlan.is_active == True).subquery()
    )
    if customer_id:
        count_query = count_query.where(InstallmentPlan.customer_id == customer_id)
    if status:
        count_query = count_query.where(InstallmentPlan.status == status)

    total = (await db.execute(count_query)).scalar()

    query = query.order_by(InstallmentPlan.created_at.desc())
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


@router.post("/installment-plans", response_model=InstallmentPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_installment_plan(
    plan_data: InstallmentPlanCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("collections:create"))
):
    plan = InstallmentPlan(
        customer_id=plan_data.customer_id,
        total_amount=plan_data.total_amount,
        down_payment=plan_data.down_payment,
        number_of_installments=plan_data.number_of_installments,
        frequency=plan_data.frequency,
        status=plan_data.status,
    )
    db.add(plan)
    await db.flush()

    remaining = plan_data.total_amount - plan_data.down_payment
    installment_amount = remaining / plan_data.number_of_installments

    frequency_days = {
        "weekly": 7,
        "biweekly": 14,
        "monthly": 30,
        "quarterly": 90,
    }
    days = frequency_days.get(plan_data.frequency.lower(), 30)
    base_date = datetime.utcnow()

    for i in range(1, plan_data.number_of_installments + 1):
        installment = Installment(
            plan_id=plan.id,
            installment_number=i,
            due_date=base_date + timedelta(days=days * i),
            amount=installment_amount,
        )
        db.add(installment)

    await db.commit()
    await db.refresh(plan)
    return plan


@router.get("/settlements", response_model=PaginatedResponse[SettlementResponse])
async def list_settlements(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    customer_id: Optional[UUID] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("collections:read"))
):
    query = select(Settlement).where(Settlement.is_active == True)

    if customer_id:
        query = query.where(Settlement.customer_id == customer_id)

    count_query = select(func.count()).select_from(
        select(Settlement.id).where(Settlement.is_active == True).subquery()
    )
    if customer_id:
        count_query = count_query.where(Settlement.customer_id == customer_id)

    total = (await db.execute(count_query)).scalar()

    query = query.order_by(Settlement.created_at.desc())
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


@router.post("/settlements", response_model=SettlementResponse, status_code=status.HTTP_201_CREATED)
async def create_settlement(
    settlement_data: SettlementCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("collections:create"))
):
    settlement = Settlement(
        customer_id=settlement_data.customer_id,
        original_amount=settlement_data.original_amount,
        settled_amount=settlement_data.settled_amount,
        discount_percentage=settlement_data.discount_percentage,
        discount_amount=settlement_data.discount_amount,
        settlement_date=settlement_data.settlement_date,
        approved_by=current_user.id,
        reason=settlement_data.reason,
    )
    db.add(settlement)
    await db.commit()
    await db.refresh(settlement)
    return settlement


@router.get("/write-offs", response_model=PaginatedResponse[WriteOffResponse])
async def list_write_offs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    customer_id: Optional[UUID] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("collections:read"))
):
    query = select(WriteOff).where(WriteOff.is_active == True)

    if customer_id:
        query = query.where(WriteOff.customer_id == customer_id)

    count_query = select(func.count()).select_from(
        select(WriteOff.id).where(WriteOff.is_active == True).subquery()
    )
    if customer_id:
        count_query = count_query.where(WriteOff.customer_id == customer_id)

    total = (await db.execute(count_query)).scalar()

    query = query.order_by(WriteOff.created_at.desc())
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


@router.post("/write-offs", response_model=WriteOffResponse, status_code=status.HTTP_201_CREATED)
async def create_write_off(
    write_off_data: WriteOffCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("collections:create"))
):
    write_off = WriteOff(
        customer_id=write_off_data.customer_id,
        amount=write_off_data.amount,
        reason=write_off_data.reason,
        approved_by=current_user.id,
        approved_at=datetime.utcnow(),
        written_off_at=write_off_data.written_off_at,
    )
    db.add(write_off)
    await db.commit()
    await db.refresh(write_off)
    return write_off


@router.post("/upload-excel", response_model=MessageResponse)
async def upload_collections_excel(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("collections:create"))
):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Only Excel files are allowed")

    try:
        import openpyxl
        content = await file.read()
        wb = openpyxl.load_workbook(io.BytesIO(content))
        ws = wb.active

        rows = list(ws.iter_rows(values_only=True))
        if len(rows) < 2:
            raise HTTPException(status_code=400, detail="Excel file is empty or has no data rows")

        headers = [str(h).strip().lower() if h else '' for h in rows[0]]
        collection_service = CollectionService(db)
        count = 0

        for row in rows[1:]:
            row_dict = dict(zip(headers, row))
            try:
                invoice_date = row_dict.get('invoice_date') or row_dict.get('تاريخ الفاتورة') or datetime.now()
                due_date = row_dict.get('due_date') or row_dict.get('تاريخ الاستحقاق') or datetime.now()
                amount = float(row_dict.get('amount') or row_dict.get('المبلغ') or 0)

                if isinstance(invoice_date, str):
                    invoice_date = datetime.fromisoformat(invoice_date.replace('Z', '+00:00'))
                if isinstance(due_date, str):
                    due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))

                data = InvoiceCreate(
                    customer_id=UUID(str(row_dict.get('customer_id') or '00000000-0000-0000-0000-000000000000')),
                    invoice_number=str(row_dict.get('invoice_number') or row_dict.get('رقم الفاتورة') or f"COL-{count+1}"),
                    invoice_date=invoice_date,
                    due_date=due_date,
                    amount=amount,
                    paid_amount=float(row_dict.get('paid_amount') or row_dict.get('المدفوع') or 0),
                    balance=amount - float(row_dict.get('paid_amount') or row_dict.get('المدفوع') or 0),
                    status=str(row_dict.get('status') or row_dict.get('الحالة') or 'new'),
                )
                await collection_service.create_invoice(data)
                count += 1
            except Exception:
                continue

        return MessageResponse(message=f"Uploaded {count} collection invoices successfully")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing Excel file: {str(e)}")
