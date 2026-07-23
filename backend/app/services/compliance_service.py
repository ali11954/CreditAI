from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.compliance import KYCRecord, AMLCheck, ComplianceCase


class ComplianceService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_kyc_records(
        self,
        customer_id: UUID,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[KYCRecord], int]:
        query = select(KYCRecord).where(KYCRecord.customer_id == customer_id)
        
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        records = result.scalars().all()
        
        return records, total
    
    async def get_kyc_record(self, record_id: UUID) -> Optional[KYCRecord]:
        result = await self.db.execute(
            select(KYCRecord).where(KYCRecord.id == record_id)
        )
        return result.scalar_one_or_none()
    
    async def create_kyc_record(self, customer_id: UUID, record_data: dict) -> KYCRecord:
        record = KYCRecord(
            customer_id=customer_id,
            **record_data
        )
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return record
    
    async def get_aml_checks(
        self,
        customer_id: UUID,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[AMLCheck], int]:
        query = select(AMLCheck).where(AMLCheck.customer_id == customer_id)
        
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        checks = result.scalars().all()
        
        return checks, total
    
    async def run_aml_check(self, customer_id: UUID, check_data: dict) -> AMLCheck:
        check = AMLCheck(
            customer_id=customer_id,
            **check_data
        )
        self.db.add(check)
        await self.db.commit()
        await self.db.refresh(check)
        return check
    
    async def get_compliance_cases(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None
    ) -> Tuple[List[ComplianceCase], int]:
        query = select(ComplianceCase)
        
        if status:
            query = query.where(ComplianceCase.status == status)
        
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        cases = result.scalars().all()
        
        return cases, total
    
    async def get_compliance_case(self, case_id: UUID) -> Optional[ComplianceCase]:
        result = await self.db.execute(
            select(ComplianceCase).where(ComplianceCase.id == case_id)
        )
        return result.scalar_one_or_none()
    
    async def create_compliance_case(self, case_data: dict) -> ComplianceCase:
        case = ComplianceCase(**case_data)
        self.db.add(case)
        await self.db.commit()
        await self.db.refresh(case)
        return case
    
    async def update_compliance_case(
        self,
        case_id: UUID,
        case_data: dict
    ) -> Optional[ComplianceCase]:
        case = await self.get_compliance_case(case_id)
        if not case:
            return None
        
        for key, value in case_data.items():
            setattr(case, key, value)
        
        await self.db.commit()
        await self.db.refresh(case)
        return case
