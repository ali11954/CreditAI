import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class LegalCase(Base):
    __tablename__ = "legal_cases"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    case_number = Column(String(100), nullable=False, index=True)
    case_type = Column(String(100), nullable=False)
    court_name = Column(String(255), nullable=True)
    filing_date = Column(DateTime, nullable=False)
    status = Column(String(50), default="open", nullable=False)
    amount_in_dispute = Column(Numeric(18, 2), nullable=True)
    currency_id = Column(UUID(as_uuid=True), ForeignKey("currencies.id"), nullable=True)
    assigned_lawyer_id = Column(UUID(as_uuid=True), ForeignKey("lawyers.id"), nullable=True)
    next_hearing_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    customer = relationship("Customer")
    currency = relationship("Currency")
    lawyer = relationship("Lawyer", foreign_keys=[assigned_lawyer_id])
    hearings = relationship("CourtHearing", back_populates="case")
    documents = relationship("LegalDocument", back_populates="case")
    judgments = relationship("LegalJudgment", back_populates="case")
    executions = relationship("LegalExecution", back_populates="case")
    timeline = relationship("LegalTimeline", back_populates="case")


class Lawyer(Base):
    __tablename__ = "lawyers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    firm_name = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    specialization = Column(String(100), nullable=True)
    license_number = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class CourtHearing(Base):
    __tablename__ = "court_hearings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("legal_cases.id"), nullable=False)
    hearing_date = Column(DateTime, nullable=False)
    hearing_time = Column(DateTime, nullable=True)
    judge = Column(String(255), nullable=True)
    outcome = Column(Text, nullable=True)
    next_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    case = relationship("LegalCase", back_populates="hearings")


class LegalDocument(Base):
    __tablename__ = "legal_documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("legal_cases.id"), nullable=False)
    document_type = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=True)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    case = relationship("LegalCase", back_populates="documents")
    uploader = relationship("User", foreign_keys=[uploaded_by])


class LegalJudgment(Base):
    __tablename__ = "legal_judgments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("legal_cases.id"), nullable=False)
    judgment_date = Column(DateTime, nullable=False)
    judgment_type = Column(String(100), nullable=False)
    amount = Column(Numeric(18, 2), nullable=True)
    description = Column(Text, nullable=True)
    appeal_deadline = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    case = relationship("LegalCase", back_populates="judgments")


class LegalExecution(Base):
    __tablename__ = "legal_executions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("legal_cases.id"), nullable=False)
    execution_type = Column(String(100), nullable=False)
    status = Column(String(50), default="pending", nullable=False)
    amount = Column(Numeric(18, 2), nullable=True)
    executed_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    case = relationship("LegalCase", back_populates="executions")


class LegalTimeline(Base):
    __tablename__ = "legal_timelines"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("legal_cases.id"), nullable=False)
    event_date = Column(DateTime, nullable=False)
    event_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    case = relationship("LegalCase", back_populates="timeline")
    creator = relationship("User", foreign_keys=[created_by])
