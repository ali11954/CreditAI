import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Exposure(Base):
    __tablename__ = "exposures"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    exposure_type = Column(String(50), nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    currency_id = Column(UUID(as_uuid=True), ForeignKey("currencies.id"), nullable=True)
    calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    details = Column(JSON, default=None)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer")
    currency = relationship("Currency")


class ConcentrationLimit(Base):
    __tablename__ = "concentration_limits"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    concentration_type = Column(String(50), nullable=False)
    category = Column(String(100), nullable=False)
    limit_amount = Column(Numeric(18, 2), nullable=False)
    utilized_amount = Column(Numeric(18, 2), default=0, nullable=False)
    currency_id = Column(UUID(as_uuid=True), ForeignKey("currencies.id"), nullable=True)
    threshold_percentage = Column(Numeric(5, 2), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    currency = relationship("Currency")


class StressTest(Base):
    __tablename__ = "stress_tests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    scenario = Column(JSON, default=None)
    results = Column(JSON, default=None)
    conducted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    conducted_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    conductor = relationship("User", foreign_keys=[conducted_by])
