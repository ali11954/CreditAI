from typing import Optional, List, Tuple
from uuid import UUID
from datetime import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def _get_or_create_default_company(self) -> UUID:
        from app.models.core import Company
        result = await self.db.execute(select(Company).limit(1))
        company = result.scalar_one_or_none()
        if company:
            return company.id
        company = Company(
            name="Default Company",
            name_ar="الشركة الافتراضية",
            registration_number="DEF001",
        )
        self.db.add(company)
        await self.db.flush()
        return company.id
    
    async def _generate_customer_code(self) -> str:
        count_result = await self.db.execute(select(func.count(Customer.id)))
        count = count_result.scalar() or 0
        return f"CUST-{count + 1:05d}"
    
    async def get_customers(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        status: Optional[str] = None,
        risk_category: Optional[str] = None,
        company_id: Optional[UUID] = None
    ) -> Tuple[List[Customer], int]:
        query = select(Customer)
        
        if search:
            query = query.where(
                (Customer.name.ilike(f"%{search}%")) |
                (Customer.name_ar.ilike(f"%{search}%")) |
                (Customer.customer_code.ilike(f"%{search}%"))
            )
        
        if status:
            query = query.where(Customer.status == status)
        
        if risk_category:
            query = query.where(Customer.risk_category == risk_category)
        
        if company_id:
            query = query.where(Customer.company_id == company_id)
        
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        customers = result.scalars().all()
        
        return customers, total
    
    async def get_customer(self, customer_id: UUID) -> Optional[Customer]:
        result = await self.db.execute(select(Customer).where(Customer.id == customer_id))
        return result.scalar_one_or_none()
    
    async def create_customer(self, data: CustomerCreate, user_id: UUID) -> Customer:
        company_id = data.company_id
        if not company_id:
            company_id = await self._get_or_create_default_company()
        
        customer_code = data.customer_code
        if not customer_code:
            customer_code = await self._generate_customer_code()
        
        customer = Customer(
            company_id=company_id,
            customer_code=customer_code,
            name=data.name,
            name_ar=data.name_ar,
            trade_name=data.trade_name,
            business_type=data.business_type,
            classification=data.classification,
            risk_category=data.risk_category,
            sales_region=data.sales_region,
            salesman_id=data.salesman_id,
            tax_id=data.tax_id,
            commercial_register=data.commercial_register,
            vat_number=data.vat_number,
            status=data.status,
            onboarding_status=data.onboarding_status,
            kyc_status=data.kyc_status,
            created_by=user_id
        )
        self.db.add(customer)
        await self.db.commit()
        await self.db.refresh(customer)
        return customer
    
    async def update_customer(
        self,
        customer_id: UUID,
        data: CustomerUpdate,
        user_id: UUID
    ) -> Optional[Customer]:
        customer = await self.get_customer(customer_id)
        if not customer:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(customer, key, value)
        
        customer.updated_by = user_id
        await self.db.commit()
        await self.db.refresh(customer)
        return customer
    
    async def delete_customer(self, customer_id: UUID) -> bool:
        customer = await self.get_customer(customer_id)
        if not customer:
            return False
        
        customer.is_active = False
        await self.db.commit()
        return True
