import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class ReportTemplate(Base):
    __tablename__ = "report_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    name_ar = Column(String(255), nullable=True)
    title_en = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    module = Column(String(100), nullable=False)
    query_template = Column(Text, nullable=False)
    parameters = Column(JSON, default=None)
    format = Column(String(20), default="pdf", nullable=False)
    icon = Column(String(50), nullable=True)
    color = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    company = relationship("Company")
    executions = relationship("ReportExecution", back_populates="template")


class ReportExecution(Base):
    __tablename__ = "report_executions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    template_id = Column(UUID(as_uuid=True), ForeignKey("report_templates.id"), nullable=False)
    executed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    parameters = Column(JSON, default=None)
    status = Column(String(50), default="pending", nullable=False)
    file_path = Column(String(500), nullable=True)
    executed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    template = relationship("ReportTemplate", back_populates="executions")
    executor = relationship("User", foreign_keys=[executed_by])


class Dashboard(Base):
    __tablename__ = "dashboards"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    name_ar = Column(String(255), nullable=True)
    layout = Column(JSON, default=None)
    widgets = Column(JSON, default=[])
    is_default = Column(Boolean, default=False, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    company = relationship("Company")
    creator = relationship("User", foreign_keys=[created_by])
    dashboard_widgets = relationship("DashboardWidget", back_populates="dashboard")


class DashboardWidget(Base):
    __tablename__ = "dashboard_widgets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dashboard_id = Column(UUID(as_uuid=True), ForeignKey("dashboards.id"), nullable=False)
    name = Column(String(255), nullable=False)
    widget_type = Column("type", String(50), nullable=False)
    config = Column(JSON, default=None)
    data_source = Column(String(255), nullable=True)
    position = Column(JSON, default={"x": 0, "y": 0})
    size = Column(JSON, default={"w": 6, "h": 4})
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    dashboard = relationship("Dashboard", back_populates="dashboard_widgets")
