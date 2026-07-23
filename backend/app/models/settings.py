import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class SystemSetting(Base):
    __tablename__ = "system_settings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(String(255), unique=True, nullable=False)
    value = Column(Text, nullable=True)
    value_type = Column(String(50), default="string", nullable=False)
    description = Column(Text, nullable=True)
    module = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class ModuleConfig(Base):
    __tablename__ = "module_configs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    module_name = Column(String(100), nullable=False)
    is_enabled = Column(Boolean, default=True, nullable=False)
    settings = Column(JSON, default=None)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    company = relationship("Company")


class MenuConfig(Base):
    __tablename__ = "menu_configs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    name_ar = Column(String(100), nullable=True)
    icon = Column(String(50), nullable=True)
    url = Column(String(255), nullable=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("menu_configs.id"), nullable=True)
    sort_order = Column(String(10), default="0", nullable=False)
    is_visible = Column(Boolean, default=True, nullable=False)
    permission_required = Column(String(100), nullable=True)
    module = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    parent = relationship("MenuConfig", remote_side=[id])
