from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class InvoiceBase(BaseModel):
    invoice_number: str
    invoice_date: datetime
    due_date: datetime
    amount: Decimal
    paid_amount: Decimal = Decimal("0")
    balance: Decimal
    currency_id: Optional[UUID] = None
    status: str = "pending"
    aging_days: int = 0
    sales_order_id: Optional[str] = None


class InvoiceCreate(InvoiceBase):
    customer_id: UUID


class InvoiceUpdate(BaseModel):
    invoice_number: Optional[str] = None
    invoice_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    amount: Optional[Decimal] = None
    paid_amount: Optional[Decimal] = None
    balance: Optional[Decimal] = None
    currency_id: Optional[UUID] = None
    status: Optional[str] = None
    aging_days: Optional[int] = None
    sales_order_id: Optional[str] = None


class InvoiceResponse(InvoiceBase):
    id: UUID
    customer_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CollectionActivityBase(BaseModel):
    activity_type: str
    direction: str = "outbound"
    subject: Optional[str] = None
    content: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    outcome: Optional[str] = None
    next_action: Optional[str] = None
    next_action_date: Optional[datetime] = None


class CollectionActivityCreate(CollectionActivityBase):
    customer_id: UUID
    invoice_id: Optional[UUID] = None
    created_by: UUID


class CollectionActivityUpdate(BaseModel):
    activity_type: Optional[str] = None
    direction: Optional[str] = None
    subject: Optional[str] = None
    content: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    outcome: Optional[str] = None
    next_action: Optional[str] = None
    next_action_date: Optional[datetime] = None


class CollectionActivityResponse(CollectionActivityBase):
    id: UUID
    customer_id: UUID
    invoice_id: Optional[UUID] = None
    created_by: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PromiseToPayBase(BaseModel):
    promise_date: datetime
    amount: Decimal
    status: str = "pending"
    notes: Optional[str] = None


class PromiseToPayCreate(PromiseToPayBase):
    customer_id: UUID
    created_by: UUID


class PromiseToPayUpdate(BaseModel):
    promise_date: Optional[datetime] = None
    amount: Optional[Decimal] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class PromiseToPayResponse(PromiseToPayBase):
    id: UUID
    customer_id: UUID
    created_by: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class InstallmentPlanBase(BaseModel):
    total_amount: Decimal
    down_payment: Decimal = Decimal("0")
    number_of_installments: int
    frequency: str
    status: str = "pending"


class InstallmentPlanCreate(InstallmentPlanBase):
    customer_id: UUID


class InstallmentPlanUpdate(BaseModel):
    total_amount: Optional[Decimal] = None
    down_payment: Optional[Decimal] = None
    number_of_installments: Optional[int] = None
    frequency: Optional[str] = None
    status: Optional[str] = None


class InstallmentPlanResponse(InstallmentPlanBase):
    id: UUID
    customer_id: UUID
    approved_by: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class InstallmentBase(BaseModel):
    installment_number: int
    due_date: datetime
    amount: Decimal
    paid_amount: Decimal = Decimal("0")
    status: str = "pending"
    paid_date: Optional[datetime] = None


class InstallmentCreate(InstallmentBase):
    plan_id: UUID


class InstallmentUpdate(BaseModel):
    installment_number: Optional[int] = None
    due_date: Optional[datetime] = None
    amount: Optional[Decimal] = None
    paid_amount: Optional[Decimal] = None
    status: Optional[str] = None
    paid_date: Optional[datetime] = None


class InstallmentResponse(InstallmentBase):
    id: UUID
    plan_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SettlementBase(BaseModel):
    original_amount: Decimal
    settled_amount: Decimal
    discount_percentage: Optional[Decimal] = None
    discount_amount: Optional[Decimal] = None
    settlement_date: datetime
    reason: Optional[str] = None


class SettlementCreate(SettlementBase):
    customer_id: UUID
    approved_by: Optional[UUID] = None


class SettlementUpdate(BaseModel):
    original_amount: Optional[Decimal] = None
    settled_amount: Optional[Decimal] = None
    discount_percentage: Optional[Decimal] = None
    discount_amount: Optional[Decimal] = None
    settlement_date: Optional[datetime] = None
    reason: Optional[str] = None


class SettlementResponse(SettlementBase):
    id: UUID
    customer_id: UUID
    approved_by: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class WriteOffBase(BaseModel):
    amount: Decimal
    reason: Optional[str] = None
    written_off_at: datetime


class WriteOffCreate(WriteOffBase):
    customer_id: UUID
    approved_by: Optional[UUID] = None


class WriteOffUpdate(BaseModel):
    amount: Optional[Decimal] = None
    reason: Optional[str] = None


class WriteOffResponse(WriteOffBase):
    id: UUID
    customer_id: UUID
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CollectionKPIBase(BaseModel):
    metric_name: str
    metric_value: Decimal
    period_start: datetime
    period_end: datetime


class CollectionKPICreate(CollectionKPIBase):
    company_id: UUID


class CollectionKPIResponse(CollectionKPIBase):
    id: UUID
    company_id: UUID
    calculated_at: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
