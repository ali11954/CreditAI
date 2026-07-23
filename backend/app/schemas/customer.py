from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class CustomerBase(BaseModel):
    customer_code: str
    name: str
    name_ar: Optional[str] = None
    trade_name: Optional[str] = None
    business_type: Optional[str] = None
    classification: Optional[str] = None
    risk_category: Optional[str] = None
    sales_region: Optional[str] = None
    salesman_id: Optional[UUID] = None
    tax_id: Optional[str] = None
    commercial_register: Optional[str] = None
    vat_number: Optional[str] = None


class CustomerCreate(BaseModel):
    name: str
    name_ar: Optional[str] = None
    customer_code: Optional[str] = None
    company_id: Optional[UUID] = None
    trade_name: Optional[str] = None
    business_type: Optional[str] = None
    classification: Optional[str] = None
    risk_category: Optional[str] = None
    sales_region: Optional[str] = None
    salesman_id: Optional[UUID] = None
    tax_id: Optional[str] = None
    commercial_register: Optional[str] = None
    vat_number: Optional[str] = None
    status: str = "pending"
    onboarding_status: str = "not_started"
    kyc_status: str = "not_verified"


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    name_ar: Optional[str] = None
    trade_name: Optional[str] = None
    business_type: Optional[str] = None
    classification: Optional[str] = None
    risk_category: Optional[str] = None
    sales_region: Optional[str] = None
    salesman_id: Optional[UUID] = None
    tax_id: Optional[str] = None
    commercial_register: Optional[str] = None
    vat_number: Optional[str] = None
    status: Optional[str] = None
    onboarding_status: Optional[str] = None
    kyc_status: Optional[str] = None
    credit_score: Optional[int] = None
    ai_score: Optional[int] = None
    extra_data: Optional[dict] = None


class CustomerResponse(CustomerBase):
    id: UUID
    company_id: UUID
    status: str
    onboarding_status: str
    kyc_status: str
    credit_score: Optional[int] = None
    ai_score: Optional[int] = None
    extra_data: Optional[dict] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CustomerContactBase(BaseModel):
    name: str
    title: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    is_primary: bool = False


class CustomerContactCreate(CustomerContactBase):
    customer_id: UUID


class CustomerContactUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    is_primary: Optional[bool] = None


class CustomerContactResponse(CustomerContactBase):
    id: UUID
    customer_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CustomerAddressBase(BaseModel):
    type: str = "primary"
    address_line1: str
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country_id: Optional[UUID] = None
    postal_code: Optional[str] = None
    is_primary: bool = False
    gps_lat: Optional[float] = None
    gps_lng: Optional[float] = None


class CustomerAddressCreate(CustomerAddressBase):
    customer_id: UUID


class CustomerAddressUpdate(BaseModel):
    type: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country_id: Optional[UUID] = None
    postal_code: Optional[str] = None
    is_primary: Optional[bool] = None
    gps_lat: Optional[float] = None
    gps_lng: Optional[float] = None


class CustomerAddressResponse(CustomerAddressBase):
    id: UUID
    customer_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CustomerBankAccountBase(BaseModel):
    bank_name: str
    account_number: str
    iban: Optional[str] = None
    swift_code: Optional[str] = None
    currency_id: Optional[UUID] = None
    is_primary: bool = False


class CustomerBankAccountCreate(CustomerBankAccountBase):
    customer_id: UUID


class CustomerBankAccountUpdate(BaseModel):
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    iban: Optional[str] = None
    swift_code: Optional[str] = None
    currency_id: Optional[UUID] = None
    is_primary: Optional[bool] = None


class CustomerBankAccountResponse(CustomerBankAccountBase):
    id: UUID
    customer_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CustomerDocumentBase(BaseModel):
    document_type: str
    document_number: Optional[str] = None
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    file_path: Optional[str] = None


class CustomerDocumentCreate(CustomerDocumentBase):
    customer_id: UUID


class CustomerDocumentUpdate(BaseModel):
    document_type: Optional[str] = None
    document_number: Optional[str] = None
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    file_path: Optional[str] = None
    is_verified: Optional[bool] = None


class CustomerDocumentResponse(CustomerDocumentBase):
    id: UUID
    customer_id: UUID
    is_verified: bool
    verified_by: Optional[UUID] = None
    verified_at: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CustomerGroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[UUID] = None


class CustomerGroupCreate(CustomerGroupBase):
    company_id: UUID


class CustomerGroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[UUID] = None


class CustomerGroupResponse(CustomerGroupBase):
    id: UUID
    company_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CustomerSegmentBase(BaseModel):
    name: str
    criteria: dict = {}


class CustomerSegmentCreate(CustomerSegmentBase):
    company_id: UUID


class CustomerSegmentUpdate(BaseModel):
    name: Optional[str] = None
    criteria: Optional[dict] = None


class CustomerSegmentResponse(CustomerSegmentBase):
    id: UUID
    company_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CustomerRelationshipBase(BaseModel):
    customer_a_id: UUID
    customer_b_id: UUID
    relationship_type: str
    description: Optional[str] = None


class CustomerRelationshipCreate(CustomerRelationshipBase):
    pass


class CustomerRelationshipUpdate(BaseModel):
    relationship_type: Optional[str] = None
    description: Optional[str] = None


class CustomerRelationshipResponse(CustomerRelationshipBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CustomerBlacklistBase(BaseModel):
    customer_id: UUID
    reason: str


class CustomerBlacklistCreate(CustomerBlacklistBase):
    added_by: UUID


class CustomerBlacklistResponse(CustomerBlacklistBase):
    id: UUID
    added_by: UUID
    added_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


class CustomerNoteBase(BaseModel):
    note: str


class CustomerNoteCreate(CustomerNoteBase):
    customer_id: UUID
    created_by: UUID


class CustomerNoteResponse(CustomerNoteBase):
    id: UUID
    customer_id: UUID
    created_by: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
