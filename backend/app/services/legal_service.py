from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.legal import LegalCase
from app.schemas.legal import LegalCaseCreate, LegalCaseUpdate


class LegalService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_cases(
        self,
        page: int = 1,
        page_size: int = 20,
        customer_id: Optional[UUID] = None,
        status: Optional[str] = None
    ) -> Tuple[List[LegalCase], int]:
        query = select(LegalCase)
        
        if customer_id:
            query = query.where(LegalCase.customer_id == customer_id)
        
        if status:
            query = query.where(LegalCase.status == status)
        
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        cases = result.scalars().all()
        
        return cases, total
    
    async def get_case(self, case_id: UUID) -> Optional[LegalCase]:
        result = await self.db.execute(
            select(LegalCase).where(LegalCase.id == case_id)
        )
        return result.scalar_one_or_none()
    
    async def create_case(
        self,
        data: LegalCaseCreate,
        user_id: UUID
    ) -> LegalCase:
        case = LegalCase(
            customer_id=data.customer_id,
            case_number=data.case_number,
            case_type=data.case_type,
            court_name=data.court_name,
            filing_date=data.filing_date,
            status=data.status,
            amount_in_dispute=data.amount_in_dispute,
            currency_id=data.currency_id,
            assigned_lawyer_id=data.assigned_lawyer_id,
            next_hearing_date=data.next_hearing_date,
            notes=data.notes,
            created_by=user_id
        )
        self.db.add(case)
        await self.db.commit()
        await self.db.refresh(case)
        return case
    
    async def update_case(
        self,
        case_id: UUID,
        data: LegalCaseUpdate
    ) -> Optional[LegalCase]:
        case = await self.get_case(case_id)
        if not case:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(case, key, value)
        
        await self.db.commit()
        await self.db.refresh(case)
        return case
    
    async def delete_case(self, case_id: UUID) -> bool:
        case = await self.get_case(case_id)
        if not case:
            return False
        
        case.is_active = False
        await self.db.commit()
        return True
