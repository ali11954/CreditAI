from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime

from app.models.credit import (
    CreditApplication, CreditAnalysis, CreditLimit, CreditLimitHistory
)
from app.models.customer import Customer
from app.models.core import Currency
from app.schemas.credit import (
    CreditApplicationCreate, CreditApplicationUpdate,
    CreditAnalysisCreate, CreditAnalysisUpdate,
    CreditLimitCreate, CreditLimitUpdate
)


class CreditService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_applications(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        status: Optional[str] = None,
        customer_id: Optional[UUID] = None
    ) -> Tuple[List[dict], int]:
        query = (
            select(
                CreditApplication,
                Customer.name.label("cust_name"),
                Customer.name_ar.label("cust_name_ar"),
                Currency.code.label("currency_code"),
            )
            .outerjoin(Customer, CreditApplication.customer_id == Customer.id)
            .outerjoin(Currency, CreditApplication.currency_id == Currency.id)
        )

        if search:
            query = query.where(CreditApplication.purpose.ilike(f"%{search}%"))

        if status:
            query = query.where(CreditApplication.status == status)

        if customer_id:
            query = query.where(CreditApplication.customer_id == customer_id)

        count_query = select(func.count()).select_from(
            select(CreditApplication.id).subquery()
        )
        total = (await self.db.execute(count_query)).scalar()

        query = query.order_by(CreditApplication.created_at.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        rows = result.all()

        enriched = []
        for row in rows:
            app = row[0]
            cust_name = row[2] or row[1]
            curr_code = row[3] or "YER_N"
            enriched.append({
                "id": app.id,
                "customer_id": app.customer_id,
                "customer_name": cust_name,
                "application_type": app.application_type,
                "requested_amount": float(app.requested_amount),
                "currency_id": app.currency_id,
                "currency_code": curr_code,
                "purpose": app.purpose,
                "status": app.status,
                "submitted_by": app.submitted_by,
                "submitted_at": app.submitted_at,
                "reviewed_by": app.reviewed_by,
                "reviewed_at": app.reviewed_at,
                "approved_by": app.approved_by,
                "approved_at": app.approved_at,
                "rejection_reason": app.rejection_reason,
                "conditions": app.conditions or [],
                "notes": app.notes,
                "is_active": app.is_active,
                "created_at": app.created_at,
                "updated_at": app.updated_at,
            })

        return enriched, total
    
    async def get_application(self, application_id: UUID) -> Optional[CreditApplication]:
        result = await self.db.execute(
            select(CreditApplication).where(CreditApplication.id == application_id)
        )
        return result.scalar_one_or_none()
    
    async def create_application(
        self,
        data: CreditApplicationCreate,
        user_id: UUID
    ) -> CreditApplication:
        application = CreditApplication(
            customer_id=data.customer_id,
            application_type=data.application_type,
            requested_amount=data.requested_amount,
            currency_id=data.currency_id,
            purpose=data.purpose,
            submitted_by=user_id,
            status="draft"
        )
        self.db.add(application)
        await self.db.commit()
        await self.db.refresh(application)
        return application
    
    async def update_application(
        self,
        application_id: UUID,
        data: CreditApplicationUpdate
    ) -> Optional[CreditApplication]:
        application = await self.get_application(application_id)
        if not application:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(application, key, value)
        
        await self.db.commit()
        await self.db.refresh(application)
        return application
    
    async def delete_application(self, application_id: UUID) -> bool:
        application = await self.get_application(application_id)
        if not application:
            return False
        
        application.is_active = False
        await self.db.commit()
        return True
    
    async def submit_application(
        self,
        application_id: UUID,
        user_id: UUID
    ) -> Optional[CreditApplication]:
        application = await self.get_application(application_id)
        if not application:
            return None
        
        application.status = "submitted"
        application.submitted_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(application)
        return application
    
    async def approve_application(
        self,
        application_id: UUID,
        user_id: UUID,
        notes: Optional[str] = None
    ) -> Optional[CreditApplication]:
        application = await self.get_application(application_id)
        if not application:
            return None
        
        application.status = "approved"
        application.approved_by = user_id
        application.approved_at = datetime.utcnow()
        if notes:
            application.notes = notes
        await self.db.commit()
        await self.db.refresh(application)
        return application
    
    async def reject_application(
        self,
        application_id: UUID,
        user_id: UUID,
        reason: str
    ) -> Optional[CreditApplication]:
        application = await self.get_application(application_id)
        if not application:
            return None
        
        application.status = "rejected"
        application.reviewed_by = user_id
        application.reviewed_at = datetime.utcnow()
        application.rejection_reason = reason
        await self.db.commit()
        await self.db.refresh(application)
        return application
    
    async def get_analyses(
        self,
        page: int = 1,
        page_size: int = 20,
        application_id: Optional[UUID] = None,
        customer_id: Optional[UUID] = None
    ) -> Tuple[List[CreditAnalysis], int]:
        query = select(CreditAnalysis)
        
        if application_id:
            query = query.where(CreditAnalysis.application_id == application_id)
        
        if customer_id:
            query = query.where(CreditAnalysis.customer_id == customer_id)
        
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        analyses = result.scalars().all()
        
        return analyses, total
    
    async def get_analysis(self, analysis_id: UUID) -> Optional[CreditAnalysis]:
        result = await self.db.execute(
            select(CreditAnalysis).where(CreditAnalysis.id == analysis_id)
        )
        return result.scalar_one_or_none()
    
    async def create_analysis(
        self,
        data: CreditAnalysisCreate,
        user_id: UUID
    ) -> CreditAnalysis:
        analysis = CreditAnalysis(
            application_id=data.application_id,
            customer_id=data.customer_id,
            analysis_type=data.analysis_type,
            financial_data=data.financial_data,
            ratios=data.ratios,
            cash_flow=data.cash_flow,
            risk_rating=data.risk_rating,
            credit_score=data.credit_score,
            ai_recommendation=data.ai_recommendation,
            analyst_id=user_id,
            analyst_notes=data.analyst_notes
        )
        self.db.add(analysis)
        await self.db.commit()
        await self.db.refresh(analysis)
        return analysis
    
    async def update_analysis(
        self,
        analysis_id: UUID,
        data: CreditAnalysisUpdate
    ) -> Optional[CreditAnalysis]:
        analysis = await self.get_analysis(analysis_id)
        if not analysis:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(analysis, key, value)
        
        await self.db.commit()
        await self.db.refresh(analysis)
        return analysis
    
    async def delete_analysis(self, analysis_id: UUID) -> bool:
        analysis = await self.get_analysis(analysis_id)
        if not analysis:
            return False
        
        analysis.is_active = False
        await self.db.commit()
        return True
    
    async def get_credit_limits(
        self,
        page: int = 1,
        page_size: int = 20,
        customer_id: Optional[UUID] = None,
        limit_type: Optional[UUID] = None
    ) -> Tuple[List[dict], int]:
        query = (
            select(
                CreditLimit,
                Customer.name.label("cust_name"),
                Customer.name_ar.label("cust_name_ar"),
                Currency.code.label("currency_code"),
            )
            .outerjoin(Customer, CreditLimit.customer_id == Customer.id)
            .outerjoin(Currency, CreditLimit.currency_id == Currency.id)
        )

        if customer_id:
            query = query.where(CreditLimit.customer_id == customer_id)

        if limit_type:
            query = query.where(CreditLimit.limit_type == limit_type)

        count_query = select(func.count()).select_from(
            select(CreditLimit.id).subquery()
        )
        total = (await self.db.execute(count_query)).scalar()

        query = query.order_by(CreditLimit.created_at.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        rows = result.all()

        enriched = []
        for row in rows:
            limit = row[0]
            cust_name = row[2] or row[1]
            curr_code = row[3] or "YER_N"
            enriched.append({
                "id": limit.id,
                "customer_id": limit.customer_id,
                "customer_name": cust_name,
                "limit_type": limit.limit_type,
                "amount": float(limit.amount),
                "currency_id": limit.currency_id,
                "currency_code": curr_code,
                "utilized_amount": float(limit.utilized_amount or 0),
                "available_amount": float(limit.available_amount or 0),
                "reserved_amount": float(limit.reserved_amount or 0),
                "start_date": limit.start_date,
                "end_date": limit.end_date,
                "status": limit.status,
                "approved_by": limit.approved_by,
                "approved_at": limit.approved_at,
                "parent_limit_id": limit.parent_limit_id,
                "is_active": limit.is_active,
                "created_at": limit.created_at,
                "updated_at": limit.updated_at,
            })

        return enriched, total
    
    async def get_credit_limit(self, limit_id: UUID) -> Optional[CreditLimit]:
        result = await self.db.execute(
            select(CreditLimit).where(CreditLimit.id == limit_id)
        )
        return result.scalar_one_or_none()
    
    async def create_credit_limit(
        self,
        data: CreditLimitCreate,
        user_id: UUID
    ) -> CreditLimit:
        limit = CreditLimit(
            customer_id=data.customer_id,
            limit_type=data.limit_type,
            amount=data.amount,
            currency_id=data.currency_id,
            available_amount=data.amount,
            start_date=data.start_date,
            end_date=data.end_date,
            approved_by=user_id,
            parent_limit_id=data.parent_limit_id
        )
        self.db.add(limit)
        await self.db.commit()
        await self.db.refresh(limit)
        return limit
    
    async def update_credit_limit(
        self,
        limit_id: UUID,
        data: CreditLimitUpdate
    ) -> Optional[CreditLimit]:
        limit = await self.get_credit_limit(limit_id)
        if not limit:
            return None
        
        old_amount = limit.amount
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(limit, key, value)
        
        if "amount" in update_data:
            history = CreditLimitHistory(
                limit_id=limit_id,
                action="update",
                old_amount=old_amount,
                new_amount=limit.amount,
                changed_by=limit.approved_by
            )
            self.db.add(history)
        
        await self.db.commit()
        await self.db.refresh(limit)
        return limit
    
    async def delete_credit_limit(self, limit_id: UUID) -> bool:
        limit = await self.get_credit_limit(limit_id)
        if not limit:
            return False
        
        limit.is_active = False
        await self.db.commit()
        return True
    
    async def get_limit_history(self, limit_id: UUID) -> List[CreditLimitHistory]:
        result = await self.db.execute(
            select(CreditLimitHistory).where(CreditLimitHistory.limit_id == limit_id)
        )
        return result.scalars().all()
