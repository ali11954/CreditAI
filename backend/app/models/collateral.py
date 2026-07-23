import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Collateral(Base):
    __tablename__ = "collaterals"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    collateral_type = Column("type", String(100), nullable=False)
    description = Column(Text, nullable=True)
    estimated_value = Column(Numeric(18, 2), nullable=True)
    assessed_value = Column(Numeric(18, 2), nullable=True)
    currency_id = Column(UUID(as_uuid=True), ForeignKey("currencies.id"), nullable=True)
    status = Column(String(50), default="active", nullable=False)
    registration_number = Column(String(100), nullable=True)
    location = Column(String(500), nullable=True)
    expiry_date = Column(DateTime, nullable=True)
    insurance_required = Column(Boolean, default=False, nullable=False)
    notes = Column(Text, nullable=True)
    images = Column(JSON, default=[])
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer")
    currency = relationship("Currency")
    valuations = relationship("CollateralValuation", back_populates="collateral")
    releases = relationship("CollateralRelease", back_populates="collateral")


class CollateralValuation(Base):
    __tablename__ = "collateral_valuations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    collateral_id = Column(UUID(as_uuid=True), ForeignKey("collaterals.id"), nullable=False)
    valuation_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    value = Column(Numeric(18, 2), nullable=False)
    methodology = Column(String(100), nullable=True)
    valuator = Column(String(255), nullable=True)
    next_valuation_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    collateral = relationship("Collateral", back_populates="valuations")


class CollateralRelease(Base):
    __tablename__ = "collateral_releases"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    collateral_id = Column(UUID(as_uuid=True), ForeignKey("collaterals.id"), nullable=False)
    released_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    released_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    reason = Column(Text, nullable=True)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    collateral = relationship("Collateral", back_populates="releases")
    releaser = relationship("User", foreign_keys=[released_by])
    approver = relationship("User", foreign_keys=[approved_by])
