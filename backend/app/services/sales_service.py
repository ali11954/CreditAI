from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from datetime import datetime

from app.models.sales import SalesInvoice
from app.models.customer import Customer
from app.models.core import Currency
from app.schemas.sales import SalesInvoiceCreate, SalesInvoiceUpdate


class SalesService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_invoices(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        status: Optional[str] = None,
        customer_id: Optional[UUID] = None
    ) -> Tuple[List[dict], int]:
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
            query = query.where(
                SalesInvoice.invoice_number.ilike(f"%{search}%")
            )
        if status:
            query = query.where(SalesInvoice.status == status)
        if customer_id:
            query = query.where(SalesInvoice.customer_id == customer_id)

        count_query = select(func.count()).select_from(
            select(SalesInvoice.id).where(SalesInvoice.is_active == True).subquery()
        )
        total = (await self.db.execute(count_query)).scalar()

        query = query.order_by(SalesInvoice.created_at.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        rows = result.all()

        enriched = []
        for row in rows:
            inv = row[0]
            cust_name_ar = row[2]
            cust_name = row[1]
            curr_code = row[3] or "YER_N"
            customer_display = cust_name_ar or cust_name

            enriched.append({
                "id": inv.id,
                "invoice_number": inv.invoice_number,
                "customer_id": inv.customer_id,
                "customer_name": customer_display,
                "invoice_date": inv.invoice_date,
                "due_date": inv.due_date,
                "amount": float(inv.amount),
                "tax_amount": float(inv.tax_amount or 0),
                "discount_amount": float(inv.discount_amount or 0),
                "total_amount": float(inv.total_amount),
                "paid_amount": float(inv.paid_amount or 0),
                "balance": float(inv.balance),
                "currency_id": inv.currency_id,
                "currency_code": curr_code,
                "status": inv.status,
                "payment_terms": inv.payment_terms,
                "notes": inv.notes,
                "product_type": inv.product_type,
                "quantity_tons": float(inv.quantity_tons) if inv.quantity_tons else None,
                "is_active": inv.is_active,
                "created_at": inv.created_at,
                "updated_at": inv.updated_at,
            })

        return enriched, total

    async def get_invoice(self, invoice_id: UUID) -> Optional[SalesInvoice]:
        result = await self.db.execute(
            select(SalesInvoice).where(SalesInvoice.id == invoice_id)
        )
        return result.scalar_one_or_none()

    async def create_invoice(self, data: SalesInvoiceCreate) -> SalesInvoice:
        invoice = SalesInvoice(
            invoice_number=data.invoice_number,
            customer_id=data.customer_id,
            invoice_date=data.invoice_date,
            due_date=data.due_date,
            amount=data.amount,
            tax_amount=data.tax_amount,
            discount_amount=data.discount_amount,
            total_amount=data.total_amount,
            paid_amount=data.paid_amount,
            balance=data.balance,
            currency_id=data.currency_id,
            status=data.status,
            payment_terms=data.payment_terms,
            notes=data.notes,
            items=data.items,
            product_type=data.product_type,
            quantity_tons=data.quantity_tons,
            company_id=data.company_id,
        )
        self.db.add(invoice)
        await self.db.commit()
        await self.db.refresh(invoice)
        return invoice

    async def update_invoice(
        self, invoice_id: UUID, data: SalesInvoiceUpdate
    ) -> Optional[SalesInvoice]:
        invoice = await self.get_invoice(invoice_id)
        if not invoice:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(invoice, key, value)

        await self.db.commit()
        await self.db.refresh(invoice)
        return invoice

    async def delete_invoice(self, invoice_id: UUID) -> bool:
        invoice = await self.get_invoice(invoice_id)
        if not invoice:
            return False

        invoice.is_active = False
        await self.db.commit()
        return True

    async def bulk_create(self, invoices_data: List[SalesInvoiceCreate]) -> int:
        count = 0
        for data in invoices_data:
            invoice = SalesInvoice(
                invoice_number=data.invoice_number,
                customer_id=data.customer_id,
                invoice_date=data.invoice_date,
                due_date=data.due_date,
                amount=data.amount,
                tax_amount=data.tax_amount,
                discount_amount=data.discount_amount,
                total_amount=data.total_amount,
                paid_amount=data.paid_amount,
                balance=data.balance,
                currency_id=data.currency_id,
                status=data.status,
                payment_terms=data.payment_terms,
                notes=data.notes,
                items=data.items,
                product_type=data.product_type,
                quantity_tons=data.quantity_tons,
                company_id=data.company_id,
            )
            self.db.add(invoice)
            count += 1
        await self.db.commit()
        return count
