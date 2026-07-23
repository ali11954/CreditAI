from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class SalesInvoiceBase(BaseModel):
    invoice_number: str
    customer_id: UUID
    invoice_date: datetime
    due_date: datetime
    amount: Decimal
    tax_amount: Decimal = Decimal("0")
    discount_amount: Decimal = Decimal("0")
    total_amount: Decimal
    paid_amount: Decimal = Decimal("0")
    balance: Decimal
    currency_id: Optional[UUID] = None
    status: str = "draft"
    payment_terms: Optional[str] = None
    notes: Optional[str] = None
    items: Optional[List[dict]] = []
    product_type: Optional[str] = None
    quantity_tons: Optional[Decimal] = None


class SalesInvoiceCreate(SalesInvoiceBase):
    company_id: Optional[UUID] = None


class SalesInvoiceUpdate(BaseModel):
    invoice_number: Optional[str] = None
    customer_id: Optional[UUID] = None
    invoice_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    amount: Optional[Decimal] = None
    tax_amount: Optional[Decimal] = None
    discount_amount: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    paid_amount: Optional[Decimal] = None
    balance: Optional[Decimal] = None
    currency_id: Optional[UUID] = None
    status: Optional[str] = None
    payment_terms: Optional[str] = None
    notes: Optional[str] = None
    items: Optional[List[dict]] = None
    product_type: Optional[str] = None
    quantity_tons: Optional[Decimal] = None


class SalesInvoiceResponse(SalesInvoiceBase):
    id: UUID
    company_id: Optional[UUID] = None
    is_active: bool
    customer_name: Optional[str] = None
    currency_code: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
