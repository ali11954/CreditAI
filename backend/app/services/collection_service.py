from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.collection import Invoice
from app.schemas.collection import InvoiceCreate, InvoiceUpdate


class CollectionService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_invoices(
        self,
        page: int = 1,
        page_size: int = 20,
        customer_id: Optional[UUID] = None,
        status: Optional[str] = None
    ) -> Tuple[List[Invoice], int]:
        query = select(Invoice)
        
        if customer_id:
            query = query.where(Invoice.customer_id == customer_id)
        
        if status:
            query = query.where(Invoice.status == status)
        
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        invoices = result.scalars().all()
        
        return invoices, total
    
    async def get_invoice(self, invoice_id: UUID) -> Optional[Invoice]:
        result = await self.db.execute(
            select(Invoice).where(Invoice.id == invoice_id)
        )
        return result.scalar_one_or_none()
    
    async def create_invoice(self, data: InvoiceCreate) -> Invoice:
        invoice = Invoice(
            customer_id=data.customer_id,
            invoice_number=data.invoice_number,
            invoice_date=data.invoice_date,
            due_date=data.due_date,
            amount=data.amount,
            paid_amount=data.paid_amount,
            balance=data.balance,
            currency_id=data.currency_id,
            status=data.status,
            aging_days=data.aging_days,
            sales_order_id=data.sales_order_id
        )
        self.db.add(invoice)
        await self.db.commit()
        await self.db.refresh(invoice)
        return invoice
    
    async def update_invoice(
        self,
        invoice_id: UUID,
        data: InvoiceUpdate
    ) -> Optional[Invoice]:
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
