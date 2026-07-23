from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db

router = APIRouter()


@router.post("/seed-database")
async def seed_database(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT count(*) FROM users"))
        user_count = result.scalar()
        if user_count and user_count > 0:
            return {"message": "Database already has users", "count": user_count}

        await db.execute(text("""
            INSERT INTO roles (id, name, name_ar, description, is_system, permissions, is_active, created_at, updated_at)
            VALUES ('53cab030-9c48-4c7b-9f4f-0d0ee7196123', 'Super Admin', 'مسؤول النظام', 'Full system access', true, '["*"]'::jsonb, true, now(), now())
            ON CONFLICT (name) DO NOTHING
        """))

        await db.execute(text("""
            INSERT INTO users (id, email, username, full_name, full_name_ar, password_hash, is_active, is_superuser, mfa_enabled, failed_login_attempts, preferences, created_at, updated_at)
            VALUES ('06e5bbd3-66fc-4df5-8784-cc38447fa31a', 'admin@creditai.com', 'admin', 'System Administrator', 'مسؤول النظام',
                    '$2b$12$kbhhRJ2fE3H67z3qZj9oJOGA8ZfuAXQPY9MHCcRfsZ2NDN.V4I2Iq',
                    true, true, false, 0, '{}'::jsonb, now(), now())
            ON CONFLICT (email) DO NOTHING
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
