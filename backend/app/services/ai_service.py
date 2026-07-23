from typing import Optional, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import random

from app.models.customer import Customer
from app.models.sales import SalesInvoice
from app.models.credit import CreditApplication


class AIService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def _get_customer_data(self, customer_id: UUID) -> Optional[Dict[str, Any]]:
        result = await self.db.execute(select(Customer).where(Customer.id == customer_id))
        customer = result.scalar_one_or_none()
        if not customer:
            return None
        
        invoices_result = await self.db.execute(
            select(SalesInvoice).where(SalesInvoice.customer_id == customer_id, SalesInvoice.is_active == True)
        )
        invoices = list(invoices_result.scalars().all())
        
        apps_result = await self.db.execute(
            select(CreditApplication).where(CreditApplication.customer_id == customer_id, CreditApplication.is_active == True)
        )
        apps = list(apps_result.scalars().all())
        
        total_invoiced = sum(float(inv.total or 0) for inv in invoices)
        total_paid = sum(float(inv.total or 0) - float(inv.balance or 0) for inv in invoices)
        total_balance = sum(float(inv.balance or 0) for inv in invoices)
        overdue = sum(1 for inv in invoices if inv.due_date and inv.due_date < datetime.utcnow() and float(inv.balance or 0) > 0)
        
        return {
            "customer_id": str(customer_id),
            "name": customer.name,
            "name_ar": customer.name_ar,
            "total_invoiced": total_invoiced,
            "total_paid": total_paid,
            "total_balance": total_balance,
            "overdue_count": overdue,
            "invoice_count": len(invoices),
            "applications_count": len(apps),
        }

    async def analyze_customer(
        self,
        customer_id: UUID,
        analysis_type: str,
        user_id: UUID
    ) -> Dict[str, Any]:
        start_time = datetime.utcnow()
        
        data = await self._get_customer_data(customer_id)
        if not data:
            raise ValueError("Customer not found")
        
        payment_ratio = data["total_paid"] / data["total_invoiced"] if data["total_invoiced"] > 0 else 0
        base_score = int(payment_ratio * 50) + 25
        risk_factor = min(data["overdue_count"] * 5, 20)
        risk_score = max(0, min(100, base_score - risk_factor + random.randint(-5, 5)))
        
        if risk_score >= 80:
            risk_level = "low"
            recommendation = "approve"
        elif risk_score >= 60:
            risk_level = "medium"
            recommendation = "approve_with_conditions"
        elif risk_score >= 40:
            risk_level = "high"
            recommendation = "review"
        else:
            risk_level = "critical"
            recommendation = "reject"
        
        factors = {
            "payment_history": "excellent" if payment_ratio > 0.9 else "good" if payment_ratio > 0.7 else "fair" if payment_ratio > 0.5 else "poor",
            "credit_utilization": "low" if data["total_balance"] < data["total_invoiced"] * 0.3 else "moderate" if data["total_balance"] < data["total_invoiced"] * 0.6 else "high",
            "overdue_status": f"{data['overdue_count']} overdue invoices",
            "payment_ratio": f"{int(payment_ratio * 100)}%",
        }
        
        result = {
            "customer_id": str(customer_id),
            "customer_name": data["name"],
            "analysis_type": analysis_type,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "credit_recommendation": recommendation,
            "financial_summary": {
                "total_invoiced": data["total_invoiced"],
                "total_paid": data["total_paid"],
                "total_balance": data["total_balance"],
                "invoice_count": data["invoice_count"],
                "overdue_count": data["overdue_count"],
            },
            "factors": factors,
            "confidence": min(95, 70 + random.randint(0, 20)),
        }
        
        return result
    
    async def calculate_credit_score(
        self,
        customer_id: UUID,
        user_id: UUID
    ) -> Dict[str, Any]:
        start_time = datetime.utcnow()
        
        data = await self._get_customer_data(customer_id)
        if not data:
            raise ValueError("Customer not found")
        
        payment_ratio = data["total_paid"] / data["total_invoiced"] if data["total_invoiced"] > 0 else 0
        
        payment_score = int(payment_ratio * 35)
        utilization_score = int(max(0, (1 - data["total_balance"] / max(data["total_invoiced"], 1))) * 25)
        history_score = min(20, data["invoice_count"] * 2)
        overdue_penalty = min(20, data["overdue_count"] * 5)
        
        score = max(0, min(100, payment_score + utilization_score + history_score - overdue_penalty + random.randint(0, 5)))
        
        if score >= 90:
            rating = "AAA"
        elif score >= 80:
            rating = "AA"
        elif score >= 70:
            rating = "A"
        elif score >= 60:
            rating = "BBB"
        elif score >= 50:
            rating = "BB"
        elif score >= 40:
            rating = "B"
        else:
            rating = "CCC"
        
        result = {
            "customer_id": str(customer_id),
            "customer_name": data["name"],
            "score": score,
            "rating": rating,
            "payment_history_score": payment_score,
            "utilization_score": utilization_score,
            "credit_age_score": history_score,
            "overdue_penalty": -overdue_penalty,
            "factors": {
                "payment_history": f"{int(payment_ratio * 100)}% payment ratio",
                "credit_mix": f"{data['invoice_count']} invoices",
                "credit_age": f"Based on {data['invoice_count']} transactions",
                "overdue_status": f"{data['overdue_count']} overdue invoices",
            },
            "recommendation": "approve" if score >= 70 else "review" if score >= 50 else "reject",
        }
        
        return result
    
    async def assess_risk_for_customer(
        self,
        customer_id: UUID,
        user_id: UUID
    ) -> Dict[str, Any]:
        data = await self._get_customer_data(customer_id)
        if not data:
            raise ValueError("Customer not found")
        
        payment_ratio = data["total_paid"] / data["total_invoiced"] if data["total_invoiced"] > 0 else 0
        risk_score = max(0, min(100, int(100 - payment_ratio * 60 + data["overdue_count"] * 10 - random.randint(0, 10))))
        
        if risk_score < 30:
            risk_level = "low"
            recommendation = "no_fraud_suspected"
        elif risk_score < 60:
            risk_level = "medium"
            recommendation = "monitor_transactions"
        else:
            risk_level = "high"
            recommendation = "investigate"
        
        suspicious_indicators = []
        if data["overdue_count"] > 2:
            suspicious_indicators.append("Multiple overdue invoices")
        if data["total_balance"] > data["total_invoiced"] * 0.8:
            suspicious_indicators.append("High outstanding balance ratio")
        if payment_ratio < 0.3:
            suspicious_indicators.append("Low payment completion rate")
        
        result = {
            "customer_id": str(customer_id),
            "customer_name": data["name"],
            "risk_level": risk_level,
            "risk_score": risk_score,
            "recommendation": recommendation,
            "suspicious_indicators": suspicious_indicators,
            "financial_summary": {
                "total_invoiced": data["total_invoiced"],
                "total_paid": data["total_paid"],
                "total_balance": data["total_balance"],
                "overdue_count": data["overdue_count"],
            },
            "confidence": min(95, 70 + random.randint(0, 20)),
        }
        
        return result
    
    async def assess_risk(
        self,
        application_id: UUID,
        user_id: UUID
    ) -> Dict[str, Any]:
        result = {
            "application_id": str(application_id),
            "risk_level": "medium",
            "risk_score": 65,
            "recommendation": "approve_with_conditions",
            "conditions": [
                "Require additional collateral",
                "Monthly financial reporting"
            ]
        }
        return result
    
    async def chat(
        self,
        message: str,
        context: Optional[Dict[str, Any]],
        user_id: UUID
    ) -> Dict[str, Any]:
        return {
            "response": f"I received your message: {message}",
            "suggestions": []
        }
