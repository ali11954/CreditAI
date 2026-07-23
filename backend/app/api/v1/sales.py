from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID
from datetime import datetime
import io

from app.database import get_db
from app.services.sales_service import SalesService
from app.schemas.sales import SalesInvoiceCreate, SalesInvoiceUpdate, SalesInvoiceResponse
from app.schemas.common import PaginatedResponse, MessageResponse
from app.dependencies import get_current_active_user, require_permission

router = APIRouter()


@router.get("/")
async def list_invoices(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    customer_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("reports:read"))
):
    sales_service = SalesService(db)
    invoices, total = await sales_service.get_invoices(
        page=page,
        page_size=page_size,
        search=search,
        status=status,
        customer_id=customer_id
    )
    return PaginatedResponse(
        items=invoices,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


@router.get("/{invoice_id}", response_model=SalesInvoiceResponse)
async def get_invoice(
    invoice_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("reports:read"))
):
    sales_service = SalesService(db)
    invoice = await sales_service.get_invoice(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.post("/", response_model=SalesInvoiceResponse, status_code=status.HTTP_201_CREATED)
async def create_invoice(
    data: SalesInvoiceCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("reports:create"))
):
    sales_service = SalesService(db)
    invoice = await sales_service.create_invoice(data)
    return invoice


@router.put("/{invoice_id}", response_model=SalesInvoiceResponse)
async def update_invoice(
    invoice_id: UUID,
    data: SalesInvoiceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("reports:update"))
):
    sales_service = SalesService(db)
    invoice = await sales_service.update_invoice(invoice_id, data)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.delete("/{invoice_id}", response_model=MessageResponse)
async def delete_invoice(
    invoice_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("reports:delete"))
):
    sales_service = SalesService(db)
    success = await sales_service.delete_invoice(invoice_id)
    if not success:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return MessageResponse(message="Invoice deleted successfully")


@router.post("/upload-excel", response_model=MessageResponse)
async def upload_sales_excel(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("reports:create"))
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
        sales_service = SalesService(db)
        count = 0

        for row in rows[1:]:
            row_dict = dict(zip(headers, row))
            try:
                invoice_date = row_dict.get('invoice_date') or row_dict.get('تاريخ الفاتورة') or datetime.now()
                due_date = row_dict.get('due_date') or row_dict.get('تاريخ الاستحقاق') or datetime.now()
                amount = float(row_dict.get('amount') or row_dict.get('المبلغ') or 0)
                tax = float(row_dict.get('tax_amount') or row_dict.get('الضريبة') or 0)
                discount = float(row_dict.get('discount_amount') or row_dict.get('الخصم') or 0)
                total = amount + tax - discount
                paid = float(row_dict.get('paid_amount') or row_dict.get('المدفوع') or 0)
                balance = total - paid

                if isinstance(invoice_date, str):
                    invoice_date = datetime.fromisoformat(invoice_date.replace('Z', '+00:00'))
                if isinstance(due_date, str):
                    due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))

                data = SalesInvoiceCreate(
                    invoice_number=str(row_dict.get('invoice_number') or row_dict.get('رقم الفاتورة') or f"INV-{count+1}"),
                    customer_id=UUID(str(row_dict.get('customer_id') or '00000000-0000-0000-0000-000000000000')),
                    invoice_date=invoice_date,
                    due_date=due_date,
                    amount=amount,
                    tax_amount=tax,
                    discount_amount=discount,
                    total_amount=total,
                    paid_amount=paid,
                    balance=balance,
                    status=str(row_dict.get('status') or row_dict.get('الحالة') or 'draft'),
                    notes=str(row_dict.get('notes') or row_dict.get('ملاحظات') or ''),
                    product_type=str(row_dict.get('product_type') or row_dict.get('نوع البضاعة') or ''),
                    quantity_tons=float(row_dict.get('quantity_tons') or row_dict.get('الكمية_بالطن') or 0) or None,
                )
                await sales_service.create_invoice(data)
                count += 1
            except Exception:
                continue

        return MessageResponse(message=f"Uploaded {count} sales invoices successfully")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing Excel file: {str(e)}")
