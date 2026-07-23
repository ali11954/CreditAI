import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class KYCRecord(Base):
    __tablename__ = "kyc_records"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    record_type = Column("type", String(50), nullable=False)
    status = Column(String(50), default="pending", nullable=False)
    verified_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    verified_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    documents = Column(JSON, default=[])
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer")
    verifier = relationship("User", foreign_keys=[verified_by])


class AMLCheck(Base):
    __tablename__ = "aml_checks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    check_type = Column(String(50), nullable=False)
    result = Column(String(50), nullable=False)
    score = Column(Integer, nullable=True)
    details = Column(JSON, default=None)
    checked_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    checked_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    customer = relationship("Customer")
    checker = relationship("User", foreign_keys=[checked_by])


class PEPCheck(Base):
    __tablename__ = "pep_checks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    is_pep = Column(Boolean, default=False, nullable=False)
    pep_type = Column(String(100), nullable=True)
    details = Column(Text, nullable=True)
    checked_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    checked_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    customer = relationship("Customer")
    checker = relationship("User", foreign_keys=[checked_by])


class SanctionCheck(Base):
    __tablename__ = "sanction_checks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    is_sanctioned = Column(Boolean, default=False, nullable=False)
    list_name = Column(String(255), nullable=True)
    details = Column(Text, nullable=True)
    checked_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    checked_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    customer = relationship("Customer")
    checker = relationship("User", foreign_keys=[checked_by])


class ComplianceCase(Base):
    __tablename__ = "compliance_cases"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    case_type = Column(String(100), nullable=False)
    status = Column(String(50), default="open", nullable=False)
    priority = Column(String(20), default="medium", nullable=False)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    due_date = Column(DateTime, nullable=True)
    resolution = Column(Text, nullable=True)
    resolution_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer")
    assignee = relationship("User", foreign_keys=[assigned_to])


class DueDiligence(Base):
    __tablename__ = "due_diligence"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    diligence_type = Column("type", String(100), nullable=False)
    status = Column(String(50), default="pending", nullable=False)
    findings = Column(JSON, default=None)
    risk_level = Column(String(20), nullable=True)
    conducted_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    conducted_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer")
    conductor = relationship("User", foreign_keys=[conducted_by])
