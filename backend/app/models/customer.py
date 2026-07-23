import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON, Numeric, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    customer_code = Column(String(50), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    name_ar = Column(String(255), nullable=True)
    trade_name = Column(String(255), nullable=True)
    business_type = Column(String(100), nullable=True)
    classification = Column(String(50), nullable=True)
    risk_category = Column(String(50), nullable=True)
    sales_region = Column(String(100), nullable=True)
    salesman_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    tax_id = Column(String(100), nullable=True)
    commercial_register = Column(String(100), nullable=True)
    vat_number = Column(String(100), nullable=True)
    status = Column(String(50), default="pending", nullable=False)
    onboarding_status = Column(String(50), default="not_started", nullable=False)
    kyc_status = Column(String(50), default="not_verified", nullable=False)
    credit_score = Column(Integer, nullable=True)
    ai_score = Column(Integer, nullable=True)
    extra_data = Column("metadata", JSON, default=None)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    contacts = relationship("CustomerContact", back_populates="customer")
    addresses = relationship("CustomerAddress", back_populates="customer")
    bank_accounts = relationship("CustomerBankAccount", back_populates="customer")
    documents = relationship("CustomerDocument", back_populates="customer")
    notes = relationship("CustomerNote", back_populates="customer")
    salesman = relationship("User", foreign_keys=[salesman_id], viewonly=True)


class CustomerContact(Base):
    __tablename__ = "customer_contacts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    name = Column(String(255), nullable=False)
    title = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    mobile = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    is_primary = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer", back_populates="contacts")


class CustomerAddress(Base):
    __tablename__ = "customer_addresses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    address_type = Column("type", String(50), default="primary")
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country_id = Column(UUID(as_uuid=True), ForeignKey("countries.id"), nullable=True)
    postal_code = Column(String(20), nullable=True)
    is_primary = Column(Boolean, default=False, nullable=False)
    gps_lat = Column(Numeric(10, 8), nullable=True)
    gps_lng = Column(Numeric(11, 8), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer", back_populates="addresses")
    country = relationship("Country")


class CustomerBankAccount(Base):
    __tablename__ = "customer_bank_accounts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    bank_name = Column(String(255), nullable=False)
    account_number = Column(String(100), nullable=False)
    iban = Column(String(50), nullable=True)
    swift_code = Column(String(20), nullable=True)
    currency_id = Column(UUID(as_uuid=True), ForeignKey("currencies.id"), nullable=True)
    is_primary = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer", back_populates="bank_accounts")
    currency = relationship("Currency")


class CustomerDocument(Base):
    __tablename__ = "customer_documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    document_type = Column(String(100), nullable=False)
    document_number = Column(String(100), nullable=True)
    issue_date = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=True)
    file_path = Column(String(500), nullable=True)
    is_verified = Column(Boolean, default=False, nullable=False)
    verified_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer", back_populates="documents")
    verifier = relationship("User", foreign_keys=[verified_by])


class CustomerGroup(Base):
    __tablename__ = "customer_groups"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("customer_groups.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    parent = relationship("CustomerGroup", remote_side=[id], foreign_keys=[parent_id])


class CustomerSegment(Base):
    __tablename__ = "customer_segments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    name = Column(String(255), nullable=False)
    criteria = Column(JSON, default=None)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class CustomerRelationship(Base):
    __tablename__ = "customer_relationships"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_a_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    customer_b_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    relationship_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    customer_a = relationship("Customer", foreign_keys=[customer_a_id])
    customer_b = relationship("Customer", foreign_keys=[customer_b_id])


class CustomerBlacklist(Base):
    __tablename__ = "customer_blacklist"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    reason = Column(Text, nullable=False)
    added_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    customer = relationship("Customer")
    added_by_user = relationship("User", foreign_keys=[added_by])


class CustomerNote(Base):
    __tablename__ = "customer_notes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    note = Column(Text, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer", back_populates="notes")
    author = relationship("User", foreign_keys=[created_by])
