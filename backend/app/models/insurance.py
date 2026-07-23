import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class InsuranceCompany(Base):
    __tablename__ = "insurance_companies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    name_ar = Column(String(255), nullable=True)
    license_number = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    address = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    policies = relationship("InsurancePolicy", back_populates="insurance_company")


class InsurancePolicy(Base):
    __tablename__ = "insurance_policies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    insurance_company_id = Column(UUID(as_uuid=True), ForeignKey("insurance_companies.id"), nullable=False)
    policy_number = Column(String(100), nullable=False)
    policy_type = Column(String(100), nullable=False)
    coverage_amount = Column(Numeric(18, 2), nullable=True)
    premium = Column(Numeric(18, 2), nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    status = Column(String(50), default="active", nullable=False)
    documents = Column(JSON, default=[])
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer")
    insurance_company = relationship("InsuranceCompany", back_populates="policies")
    claims = relationship("InsuranceClaim", back_populates="policy")


class InsuranceClaim(Base):
    __tablename__ = "insurance_claims"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    policy_id = Column(UUID(as_uuid=True), ForeignKey("insurance_policies.id"), nullable=False)
    claim_number = Column(String(100), nullable=False)
    claim_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    amount = Column(Numeric(18, 2), nullable=True)
    status = Column(String(50), default="pending", nullable=False)
    description = Column(Text, nullable=True)
    resolution = Column(Text, nullable=True)
    resolved_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    policy = relationship("InsurancePolicy", back_populates="claims")
