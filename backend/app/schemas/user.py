from typing import Optional, List
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    full_name_ar: Optional[str] = None
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str
    is_active: bool = True
    is_superuser: bool = False
    role_id: Optional[UUID] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    full_name_ar: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    is_active: Optional[bool] = None
    preferences: Optional[dict] = None
    role_id: Optional[UUID] = None


class UserResponse(UserBase):
    id: UUID
    avatar: Optional[str] = None
    is_active: bool
    is_superuser: bool
    mfa_enabled: bool
    role: Optional[str] = None
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class RoleBase(BaseModel):
    name: str
    name_ar: Optional[str] = None
    description: Optional[str] = None
    is_system: bool = False


class RoleCreate(RoleBase):
    permissions: List[str] = []


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    name_ar: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[List[str]] = None


class RoleResponse(RoleBase):
    id: UUID
    is_active: bool
    permissions: List[str] = []
    users_count: int = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None
    module: str
    action: str


class PermissionCreate(PermissionBase):
    pass


class PermissionResponse(PermissionBase):
    id: UUID
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserRoleAssign(BaseModel):
    user_id: UUID
    role_id: UUID


class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None
    leader_id: Optional[UUID] = None


class TeamCreate(TeamBase):
    member_ids: List[UUID] = []


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    leader_id: Optional[UUID] = None
    member_ids: Optional[List[UUID]] = None


class TeamResponse(TeamBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DelegationBase(BaseModel):
    from_user_id: UUID
    to_user_id: UUID
    start_date: datetime
    end_date: datetime
    permissions: List[str] = []


class DelegationCreate(DelegationBase):
    pass


class DelegationResponse(DelegationBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class LoginHistoryResponse(BaseModel):
    id: UUID
    user_id: UUID
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    login_at: datetime
    logout_at: Optional[datetime] = None
    is_success: bool
    
    class Config:
        from_attributes = True


class ActiveSessionResponse(BaseModel):
    id: UUID
    user_id: UUID
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime
    expires_at: datetime
    
    class Config:
        from_attributes = True


class DigitalSignatureBase(BaseModel):
    signature_image: Optional[str] = None
    certificate_data: Optional[str] = None


class DigitalSignatureCreate(DigitalSignatureBase):
    pass


class DigitalSignatureResponse(DigitalSignatureBase):
    id: UUID
    user_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
