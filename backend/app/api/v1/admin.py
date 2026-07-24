from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db

router = APIRouter()


@router.post("/seed-database")
async def seed_database(force: bool = False, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT count(*) FROM users"))
        user_count = result.scalar()
        if user_count and user_count > 0 and not force:
            return {"message": "Database already has users. Use ?force=true to update password.", "count": user_count}

        await db.execute(text("""
            INSERT INTO roles (id, name, name_ar, description, is_system, permissions, is_active, created_at, updated_at)
            VALUES ('53cab030-9c48-4c7b-9f4f-0d0ee7196123', 'Super Admin', 'مسؤول النظام', 'Full system access', true, '["*"]'::jsonb, true, now(), now())
            ON CONFLICT (name) DO NOTHING
        """))

        await db.execute(text("""
            INSERT INTO users (id, email, username, full_name, full_name_ar, password_hash, is_active, is_superuser, mfa_enabled, failed_login_attempts, preferences, created_at, updated_at)
            VALUES ('06e5bbd3-66fc-4df5-8784-cc38447fa31a', 'admin@creditai.com', 'admin', 'System Administrator', 'مسؤول النظام',
                    '$2b$12$GygHfz/94f5Kp875MD1yTO8ZbAcizXE/yhF/XOakscR65wLmErXXW',
                    true, true, false, 0, '{}'::jsonb, now(), now())
            ON CONFLICT (email) DO UPDATE SET password_hash = '$2b$12$GygHfz/94f5Kp875MD1yTO8ZbAcizXE/yhF/XOakscR65wLmErXXW', is_active = true, is_superuser = true
        """))

        await db.execute(text("""
            INSERT INTO user_roles (user_id, role_id, assigned_at)
            VALUES ('06e5bbd3-66fc-4df5-8784-cc38447fa31a', '53cab030-9c48-4c7b-9f4f-0d0ee7196123', now())
            ON CONFLICT (user_id, role_id) DO NOTHING
        """))

        await db.execute(text("""
            INSERT INTO currencies (id, code, name, name_ar, symbol, is_base, exchange_rate, is_active, created_at, updated_at)
            VALUES
            ('fb9444bd-8793-4f90-875e-72f422d6885b', 'YER_N', 'Yemeni Rial (North)', 'ريال يمني شمالي', '﷼', true, 1.000000, true, now(), now()),
            ('f4c1ddfb-290b-42d2-8ab2-e17240b1ec51', 'YER_S', 'Yemeni Rial (South)', 'ريال يمني جنوبي', '﷼', false, 3.000000, true, now(), now()),
            ('4058f587-f9cf-4dfc-8f65-0a3942f5f991', 'SAR', 'Saudi Riyal', 'ريال سعودي', '﷼', false, 0.100000, true, now(), now()),
            ('2a5bfca5-fbec-467e-b339-5f8ef5670f2b', 'USD', 'US Dollar', 'دولار أمريكي', '$', false, 0.004000, true, now(), now())
            ON CONFLICT (code) DO NOTHING
        """))

        await db.execute(text("""
            INSERT INTO report_templates (id, name, name_ar, description, module, query_template, parameters, format, is_active, created_at, updated_at, title_en, icon, color)
            VALUES
            ('d08e4b96-2055-4049-823f-ad7bc3596abe', 'Customer Summary Report', 'تقرير ملخص العملاء', 'تقرير شامل بالعملاء', 'customers', 'SELECT * FROM customers', NULL, 'pdf', true, now(), now(), 'Customer Summary Report', 'Users', 'text-blue-500'),
            ('5c4e124e-5f07-4c90-b296-bcf82310b492', 'Credit Applications Report', 'تقرير طلبات الائتمان', 'تقرير بطلبات الائتمان', 'credit', 'SELECT * FROM credit_applications', NULL, 'pdf', true, now(), now(), 'Credit Applications Report', 'FileText', 'text-green-500'),
            ('6fabfb5d-0ac4-4eca-9b0d-516e4f7e9759', 'Credit Limits Report', 'تقرير حدود الائتمان', 'تقرير بحدود الائتمان', 'credit', 'SELECT * FROM credit_limits', NULL, 'pdf', true, now(), now(), 'Credit Limits Report', 'CreditCard', 'text-purple-500'),
            ('916ee69a-ee44-47f5-bc34-48a5353636db', 'Collections Report', 'تقرير التحصيل', 'تقرير التحصيل المفصل', 'collections', 'SELECT * FROM invoices', NULL, 'pdf', true, now(), now(), 'Collections Report', 'TrendingUp', 'text-orange-500'),
            ('97298c17-d68b-469c-87fb-e275e23e2368', 'Aging Report', 'تقرير التقادم', 'تحليل الديون المتأخرة', 'collections', 'SELECT * FROM invoices ORDER BY aging_days', NULL, 'pdf', true, now(), now(), 'Aging Report', 'BarChart3', 'text-red-500'),
            ('9b228f95-8293-4b17-8ff9-1709acad3f68', 'Risk Assessment Report', 'تقرير المخاطر', 'تقييم المخاطر الائتمانية', 'compliance', 'SELECT * FROM customers', NULL, 'pdf', true, now(), now(), 'Risk Assessment Report', 'AlertTriangle', 'text-yellow-500'),
            ('82733962-53a9-43fc-95e6-be5ef5f8e228', 'Legal Cases Report', 'تقرير القضايا القانونية', 'تقرير القضايا', 'legal', 'SELECT * FROM legal_cases', NULL, 'pdf', true, now(), now(), 'Legal Cases Report', 'Scale', 'text-indigo-500'),
            ('0bdb0525-426f-466f-ac23-372708b70664', 'Document Registry Report', 'تقرير الوثائق', 'سجل الوثائق', 'documents', 'SELECT * FROM documents', NULL, 'pdf', true, now(), now(), 'Document Registry Report', 'FolderOpen', 'text-teal-500'),
            ('4e450b30-a98c-4f66-8e39-08b0dbac939a', 'Audit Trail Report', 'تقرير سجل التدقيق', 'تقرير التدقيق الشامل', 'audit', 'SELECT * FROM audit_logs', NULL, 'pdf', true, now(), now(), 'Audit Trail Report', 'History', 'text-gray-500')
            ON CONFLICT (id) DO NOTHING
        """))

        await db.commit()
        return {"message": "Database seeded successfully!", "users": ["admin@creditai.com / Admin@123"]}

    except Exception as e:
        await db.rollback()
        return {"error": str(e)}


@router.post("/seed-demo-data")
async def seed_demo_data(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT id FROM companies LIMIT 1"))
        existing = result.scalar_one_or_none()
        if existing:
            return {"message": "Demo data already exists"}

        company_id = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        admin_id = "06e5bbd3-66fc-4df5-8784-cc38447fa31a"

        await db.execute(text("""
            INSERT INTO companies (id, name, name_ar, registration_number, is_active, created_at, updated_at)
            VALUES ('""" + company_id + """', 'CreditAI Corp', 'شركة كريديت أي آي', 'CR-001', true, now(), now())
            ON CONFLICT (id) DO NOTHING
        """))

        customers = [
            {"code": "CUST-00001", "name": "Al-Noor Trading Co.", "name_ar": "شركة النور للتجارة", "type": "Trading", "classification": "gold", "risk": "low", "score": 85, "status": "active", "region": "Sana'a"},
            {"code": "CUST-00002", "name": "Yemen Gulf Construction", "name_ar": "شركة الخليج اليمنية للمقاولات", "type": "Construction", "classification": "platinum", "risk": "low", "score": 92, "status": "active", "region": "Aden"},
            {"code": "CUST-00003", "name": "Al-Baraka Foods", "name_ar": "شركة البركة للأغذية", "type": "Food & Beverage", "classification": "silver", "risk": "medium", "score": 68, "status": "active", "region": "Taiz"},
            {"code": "CUST-00004", "name": "Hadramout Oil & Gas", "name_ar": "شركة حضرموت للنفط والغاز", "type": "Oil & Gas", "classification": "platinum", "risk": "low", "score": 95, "status": "active", "region": "Hadramout"},
            {"code": "CUST-00005", "name": "Saba Tech Solutions", "name_ar": "سبأ للحلول التقنية", "type": "Technology", "classification": "gold", "risk": "medium", "score": 75, "status": "active", "region": "Sana'a"},
            {"code": "CUST-00006", "name": "Red Sea Hotels Group", "name_ar": "مجموعة فنادق البحر الأحمر", "type": "Hospitality", "classification": "silver", "risk": "medium", "score": 70, "status": "pending", "region": "Hodeidah"},
            {"code": "CUST-00007", "name": "Al-Thawra Agricultural", "name_ar": "شركة الثورة الزراعية", "type": "Agriculture", "classification": "bronze", "risk": "high", "score": 45, "status": "active", "region": "Ibb"},
            {"code": "CUST-00008", "name": "Future Pharma Yemen", "name_ar": "فيوتشر فارما اليمن", "type": "Pharmaceutical", "classification": "gold", "risk": "low", "score": 88, "status": "active", "region": "Sana'a"},
            {"code": "CUST-00009", "name": "National Logistics Co.", "name_ar": "شركة الناشونال للخدمات اللوجستية", "type": "Logistics", "classification": "standard", "risk": "high", "score": 35, "status": "inactive", "region": "Aden"},
            {"code": "CUST-00010", "name": "Smart City Developers", "name_ar": "مطوري المدينة الذكية", "type": "Real Estate", "classification": "silver", "risk": "medium", "score": 62, "status": "active", "region": "Sana'a"},
        ]

        for c in customers:
            await db.execute(text(f"""
                INSERT INTO customers (id, company_id, customer_code, name, name_ar, business_type, classification, risk_category, credit_score, status, sales_region, onboarding_status, kyc_status, is_active, created_by, created_at, updated_at)
                VALUES (gen_random_uuid(), '{company_id}', '{c["code"]}', '{c["name"]}', '{c["name_ar"]}', '{c["type"]}', '{c["classification"]}', '{c["risk"]}', {c["score"]}, '{c["status"]}', '{c["region"]}', 'completed', 'verified', true, '{admin_id}', now(), now())
                ON CONFLICT (customer_code) DO NOTHING
            """))

        await db.commit()
        return {"message": "Demo data seeded successfully!", "customers": len(customers)}

    except Exception as e:
        await db.rollback()
        return {"error": str(e)}
