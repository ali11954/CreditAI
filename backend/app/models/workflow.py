import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class WorkflowTemplate(Base):
    __tablename__ = "workflow_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    module = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    steps = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    instances = relationship("WorkflowInstance", back_populates="template")


class WorkflowInstance(Base):
    __tablename__ = "workflow_instances"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    template_id = Column(UUID(as_uuid=True), ForeignKey("workflow_templates.id"), nullable=False)
    entity_type = Column(String(100), nullable=False)
    entity_id = Column(UUID(as_uuid=True), nullable=False)
    status = Column(String(50), default="in_progress", nullable=False)
    current_step = Column(Integer, default=1, nullable=False)
    initiated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    initiated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    template = relationship("WorkflowTemplate", back_populates="instances")
    initiator = relationship("User", foreign_keys=[initiated_by])
    steps = relationship("WorkflowStep", back_populates="instance")


class WorkflowStep(Base):
    __tablename__ = "workflow_steps"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instance_id = Column(UUID(as_uuid=True), ForeignKey("workflow_instances.id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    assignee_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    status = Column(String(50), default="pending", nullable=False)
    action = Column(String(50), nullable=True)
    comments = Column(Text, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    instance = relationship("WorkflowInstance", back_populates="steps")
    assignee = relationship("User", foreign_keys=[assignee_id])


class ApprovalMatrix(Base):
    __tablename__ = "approval_matrices"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    module = Column(String(100), nullable=False)
    action = Column(String(100), nullable=False)
    conditions = Column(JSON, default=None)
    approvers = Column(JSON, default=[])
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
