from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from datetime import datetime


class CurrencyBase(BaseModel):
    code: str
    name: str
    name_ar: Optional[str] = None
    symbol: Optional[str] = None
    is_base: bool = False
    exchange_rate: Decimal = Decimal("1.0")
    is_active: bool = True


class CurrencyCreate(CurrencyBase):
    pass


class CurrencyUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    name_ar: Optional[str] = None
    symbol: Optional[str] = None
    is_base: Optional[bool] = None
    exchange_rate: Optional[Decimal] = None
    is_active: Optional[bool] = None


class CurrencyResponse(CurrencyBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
