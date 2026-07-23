import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON, Numeric, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    invoice_number = Column(String(100), nullable=False, index=True)
    invoice_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    paid_amount = Column(Numeric(18, 2), default=0, nullable=False)
    balance = Column(Numeric(18, 2), nullable=False)
    currency_id = Column(UUID(as_uuid=True), ForeignKey("currencies.id"), nullable=True)
    status = Column(String(50), default="pending", nullable=False)
    aging_days = Column(Integer, default=0, nullable=False)
    sales_order_id = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer")
    currency = relationship("Currency")
    activities = relationship("CollectionActivity", back_populates="invoice")


class CollectionActivity(Base):
    __tablename__ = "collection_activities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    invoice_id = Column(UUID(as_uuid=True), ForeignKey("invoices.id"), nullable=True)
    activity_type = Column(String(50), nullable=False)
    direction = Column(String(20), default="outbound")
    subject = Column(String(255), nullable=True)
    content = Column(Text, nullable=True)
    scheduled_date = Column(DateTime, nullable=True)
    completed_date = Column(DateTime, nullable=True)
    outcome = Column(String(100), nullable=True)
    next_action = Column(String(255), nullable=True)
    next_action_date = Column(DateTime, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer")
    invoice = relationship("Invoice", back_populates="activities")
    creator = relationship("User", foreign_keys=[created_by])


class PromiseToPay(Base):
    __tablename__ = "promises_to_pay"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    promise_date = Column(DateTime, nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    status = Column(String(50), default="pending", nullable=False)
    notes = Column(Text, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer")
    creator = relationship("User", foreign_keys=[created_by])


class InstallmentPlan(Base):
    __tablename__ = "installment_plans"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    total_amount = Column(Numeric(18, 2), nullable=False)
    down_payment = Column(Numeric(18, 2), default=0, nullable=False)
    number_of_installments = Column(Integer, nullable=False)
    frequency = Column(String(50), nullable=False)
    status = Column(String(50), default="pending", nullable=False)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer")
    approver = relationship("User", foreign_keys=[approved_by])
    installments = relationship("Installment", back_populates="plan")


class Installment(Base):
    __tablename__ = "installments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id = Column(UUID(as_uuid=True), ForeignKey("installment_plans.id"), nullable=False)
    installment_number = Column(Integer, nullable=False)
    due_date = Column(DateTime, nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    paid_amount = Column(Numeric(18, 2), default=0, nullable=False)
    status = Column(String(50), default="pending", nullable=False)
    paid_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    plan = relationship("InstallmentPlan", back_populates="installments")


class Settlement(Base):
    __tablename__ = "settlements"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    original_amount = Column(Numeric(18, 2), nullable=False)
    settled_amount = Column(Numeric(18, 2), nullable=False)
    discount_percentage = Column(Numeric(5, 2), nullable=True)
    discount_amount = Column(Numeric(18, 2), nullable=True)
    settlement_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    reason = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer")
    approver = relationship("User", foreign_keys=[approved_by])


class WriteOff(Base):
    __tablename__ = "write_offs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    reason = Column(Text, nullable=True)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    written_off_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer")
    approver = relationship("User", foreign_keys=[approved_by])


class CollectionKPI(Base):
    __tablename__ = "collection_kpis"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Numeric(18, 4), nullable=False)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    company = relationship("Company")
