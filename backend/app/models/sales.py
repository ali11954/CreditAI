import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON, Numeric, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class SalesInvoice(Base):
    __tablename__ = "sales_invoices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_number = Column(String(100), nullable=False, index=True, unique=True)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    invoice_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    tax_amount = Column(Numeric(18, 2), default=0, nullable=False)
    discount_amount = Column(Numeric(18, 2), default=0, nullable=False)
    total_amount = Column(Numeric(18, 2), nullable=False)
    paid_amount = Column(Numeric(18, 2), default=0, nullable=False)
    balance = Column(Numeric(18, 2), nullable=False)
    currency_id = Column(UUID(as_uuid=True), ForeignKey("currencies.id"), nullable=True)
    status = Column(String(50), default="draft", nullable=False)
    payment_terms = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    items = Column(JSON, default=[], nullable=True)
    product_type = Column(String(255), nullable=True)
    quantity_tons = Column(Numeric(18, 2), nullable=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    customer = relationship("Customer")
    currency = relationship("Currency")
    company = relationship("Company")
