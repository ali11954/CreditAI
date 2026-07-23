import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON, Numeric, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class CreditApplication(Base):
    __tablename__ = "credit_applications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    application_type = Column(String(50), nullable=False)
    requested_amount = Column(Numeric(18, 2), nullable=False)
    currency_id = Column(UUID(as_uuid=True), ForeignKey("currencies.id"), nullable=True)
    purpose = Column(Text, nullable=True)
    status = Column(String(50), default="draft", nullable=False)
    submitted_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    submitted_at = Column(DateTime, nullable=True)
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    conditions = Column(JSON, default=[])
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer")
    currency = relationship("Currency")
    submitter = relationship("User", foreign_keys=[submitted_by])
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    approver = relationship("User", foreign_keys=[approved_by])
    analyses = relationship("CreditAnalysis", back_populates="application")


class CreditAnalysis(Base):
    __tablename__ = "credit_analyses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey("credit_applications.id"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    analysis_type = Column(String(50), nullable=False)
    financial_data = Column(JSON, default=None)
    ratios = Column(JSON, default=None)
    cash_flow = Column(JSON, default=None)
    risk_rating = Column(String(20), nullable=True)
    credit_score = Column(Integer, nullable=True)
    ai_recommendation = Column(Text, nullable=True)
    analyst_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    analyst_notes = Column(Text, nullable=True)
    analyzed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    application = relationship("CreditApplication", back_populates="analyses")
    customer = relationship("Customer")
    analyst = relationship("User", foreign_keys=[analyst_id])


class CreditCommittee(Base):
    __tablename__ = "credit_committees"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    meeting_date = Column(DateTime, nullable=True)
    status = Column(String(50), default="active", nullable=False)
    minutes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    company = relationship("Company")
    members = relationship("CommitteeMember", back_populates="committee")
    decisions = relationship("CommitteeDecision", back_populates="committee")


class CommitteeMember(Base):
    __tablename__ = "committee_members"
    
    committee_id = Column(UUID(as_uuid=True), ForeignKey("credit_committees.id"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    role_in_committee = Column(String(50), default="member")
    is_active = Column(Boolean, default=True, nullable=False)
    assigned_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    committee = relationship("CreditCommittee", back_populates="members")
    user = relationship("User")


class CommitteeDecision(Base):
    __tablename__ = "committee_decisions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    committee_id = Column(UUID(as_uuid=True), ForeignKey("credit_committees.id"), nullable=False)
    application_id = Column(UUID(as_uuid=True), ForeignKey("credit_applications.id"), nullable=False)
    decision = Column(String(50), nullable=False)
    conditions = Column(JSON, default=[])
    voted_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    vote = Column(String(20), nullable=False)
    vote_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    comments = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    committee = relationship("CreditCommittee", back_populates="decisions")
    application = relationship("CreditApplication")
    voter = relationship("User", foreign_keys=[voted_by])


class CreditLimit(Base):
    __tablename__ = "credit_limits"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    limit_type = Column(String(50), nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    currency_id = Column(UUID(as_uuid=True), ForeignKey("currencies.id"), nullable=True)
    utilized_amount = Column(Numeric(18, 2), default=0, nullable=False)
    available_amount = Column(Numeric(18, 2), nullable=False)
    reserved_amount = Column(Numeric(18, 2), default=0, nullable=False)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    status = Column(String(50), default="active", nullable=False)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    parent_limit_id = Column(UUID(as_uuid=True), ForeignKey("credit_limits.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer")
    currency = relationship("Currency")
    approver = relationship("User", foreign_keys=[approved_by])
    parent_limit = relationship("CreditLimit", remote_side=[id])
    histories = relationship("CreditLimitHistory", back_populates="limit")


class CreditLimitHistory(Base):
    __tablename__ = "credit_limit_histories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    limit_id = Column(UUID(as_uuid=True), ForeignKey("credit_limits.id"), nullable=False)
    action = Column(String(50), nullable=False)
    old_amount = Column(Numeric(18, 2), nullable=True)
    new_amount = Column(Numeric(18, 2), nullable=True)
    reason = Column(Text, nullable=True)
    changed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    changed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    limit = relationship("CreditLimit", back_populates="histories")
    changer = relationship("User", foreign_keys=[changed_by])


class CreditScore(Base):
    __tablename__ = "credit_scores"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    score = Column(Integer, nullable=False)
    factors = Column(JSON, default=None)
    calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    methodology = Column(String(100), nullable=True)
    version = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer")
