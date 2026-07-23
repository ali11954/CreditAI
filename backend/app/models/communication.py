import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class CommunicationTemplate(Base):
    __tablename__ = "communication_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    name_ar = Column(String(255), nullable=True)
    template_type = Column("type", String(50), nullable=False)
    subject = Column(String(255), nullable=True)
    body = Column(Text, nullable=False)
    variables = Column(JSON, default=[])
    is_active = Column(Boolean, default=True, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    company = relationship("Company")


class CommunicationLog(Base):
    __tablename__ = "communication_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True)
    log_type = Column("type", String(50), nullable=False)
    direction = Column(String(20), default="outbound", nullable=False)
    recipient = Column(String(255), nullable=True)
    subject = Column(String(255), nullable=True)
    content = Column(Text, nullable=True)
    status = Column(String(50), default="sent", nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    delivered_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer")
    creator = relationship("User", foreign_keys=[created_by])


class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    campaign_type = Column("type", String(50), nullable=False)
    target_audience = Column(JSON, default=None)
    template_id = Column(UUID(as_uuid=True), ForeignKey("communication_templates.id"), nullable=True)
    scheduled_date = Column(DateTime, nullable=True)
    status = Column(String(50), default="draft", nullable=False)
    sent_count = Column(Integer, default=0, nullable=False)
    opened_count = Column(Integer, default=0, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    template = relationship("CommunicationTemplate")
    company = relationship("Company")
