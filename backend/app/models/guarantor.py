import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Guarantor(Base):
    __tablename__ = "guarantors"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    name = Column(String(255), nullable=False)
    name_ar = Column(String(255), nullable=True)
    relationship_type = Column(String(100), nullable=True)
    guarantor_type = Column(String(50), nullable=False)
    is_individual = Column(Boolean, default=True, nullable=False)
    national_id = Column(String(100), nullable=True)
    commercial_register = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    address = Column(String(500), nullable=True)
    status = Column(String(50), default="pending", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer")
    financial = relationship("GuarantorFinancial", back_populates="guarantor")
    supports = relationship("GuarantorSupport", back_populates="guarantor")


class GuarantorFinancial(Base):
    __tablename__ = "guarantor_financials"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    guarantor_id = Column(UUID(as_uuid=True), ForeignKey("guarantors.id"), nullable=False)
    assets = Column(JSON, default=None)
    liabilities = Column(JSON, default=None)
    income = Column(JSON, default=None)
    net_worth = Column(Numeric(18, 2), nullable=True)
    assessment_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    assessed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    guarantor = relationship("Guarantor", back_populates="financial")
    assessor = relationship("User", foreign_keys=[assessed_by])


class GuarantorSupport(Base):
    __tablename__ = "guarantor_supports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    guarantor_id = Column(UUID(as_uuid=True), ForeignKey("guarantors.id"), nullable=False)
    credit_application_id = Column(UUID(as_uuid=True), ForeignKey("credit_applications.id"), nullable=True)
    guarantee_type = Column(String(50), nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    currency_id = Column(UUID(as_uuid=True), ForeignKey("currencies.id"), nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    status = Column(String(50), default="active", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    guarantor = relationship("Guarantor", back_populates="supports")
    credit_application = relationship("CreditApplication")
    currency = relationship("Currency")
