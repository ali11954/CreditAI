-- CreditAI Enterprise - Seed Data for Supabase
-- Execute this in Supabase SQL Editor

-- Currencies
INSERT INTO public.currencies (id, code, name, name_ar, symbol, is_default, exchange_rate, is_active, created_at, updated_at) VALUES
('fb9444bd-8793-4f90-875e-72f422d6885b', 'YER_N', 'Yemeni Rial (North)', 'riyal yamani shamaly', 'YR', true, 1.000000, true, '2026-07-23 10:11:54.925954', '2026-07-23 10:11:54.925954'),
('f4c1ddfb-290b-42d2-8ab2-e17240b1ec51', 'YER_S', 'Yemeni Rial (South)', 'riyal yamani januby', 'YR', false, 3.000000, true, '2026-07-23 10:11:54.925954', '2026-07-23 07:30:23.484561'),
('4058f587-f9cf-4dfc-8f65-0a3942f5f991', 'SAR', 'Saudi Riyal', 'riyal saudi', 'SR', false, 0.100000, true, '2026-07-23 10:11:54.925954', '2026-07-23 10:11:54.925954'),
('2a5bfca5-fbec-467e-b339-5f8ef5670f2b', 'USD', 'US Dollar', 'dollar', 'USD', false, 0.004000, true, '2026-07-23 10:11:54.925954', '2026-07-23 10:11:54.925954');

-- Roles
INSERT INTO public.roles (id, name, name_ar, description, is_system, permissions, is_active, created_at, updated_at) VALUES
('53cab030-9c48-4c7b-9f4f-0d0ee7196123', 'Super Admin', 'مسؤول النظام', 'Full system access', true, '["*"]', true, '2026-07-23 04:19:44.075628', '2026-07-23 04:19:44.075633');

-- Users (password: Admin@123)
INSERT INTO public.users (id, email, username, full_name, full_name_ar, phone, password_hash, avatar, is_active, is_superuser, mfa_enabled, mfa_secret, last_login, failed_login_attempts, locked_until, preferences, created_at, updated_at) VALUES
('06e5bbd3-66fc-4df5-8784-cc38447fa31a', 'admin@creditai.com', 'admin', 'System Administrator', 'مسؤول النظام', NULL, '$2b$12$ZWxUzqptHanth1hAncXaIOoB7SjvhEj1PVfGRzXM3nHMcANRtvrk.', NULL, true, true, false, NULL, '2026-07-23 09:25:36.512407', 0, NULL, '{}', '2026-07-23 04:19:44.396993', '2026-07-23 09:25:36.514633');

-- User Roles
INSERT INTO public.user_roles (user_id, role_id, assigned_at) VALUES
('06e5bbd3-66fc-4df5-8784-cc38447fa31a', '53cab030-9c48-4c7b-9f4f-0d0ee7196123', '2026-07-23 04:19:44.402556');

-- Customers
INSERT INTO public.customers (id, company_id, customer_number, name, name_ar, name_en, customer_type, risk_category, cr_number, tax_id, national_id, phone, mobile, email, status, kyc_status, aml_status, segment, assigned_to, metadata, is_active, created_at, updated_at, created_by, updated_by) VALUES
('537815f3-5e3c-4245-af6b-1ef3baa07b42', '5aea2896-dfea-42f4-ae00-09e4580debc9', 'CUST-00002', 'alghith systemes', 'الغيث للانظمة', 'alghith systemes', 'trading', 'platinum', '', '', NULL, '0555454', '0154544', NULL, 'active', 'not_started', 'not_verified', NULL, NULL, '{}', true, '2026-07-23 05:51:36.256652', '2026-07-23 08:32:21.455427', '06e5bbd3-66fc-4df5-8784-cc38447fa31a', '06e5bbd3-66fc-4df5-8784-cc38447fa31a');

-- Report Templates
INSERT INTO public.report_templates (id, name, name_ar, description, category, query, parameters, format, is_active, executed_at, created_at, updated_at, title_en, icon, color) VALUES
('d08e4b96-2055-4049-823f-ad7bc3596abe', 'Customer Summary Report', 'تقرير ملخص العملاء', 'تقرير شامل يحتوي على ملخص لجميع العملاء وبياناتهم الأساسية', 'customers', 'SELECT * FROM customers', NULL, 'pdf', true, NULL, '2026-07-23 09:54:24.58495', '2026-07-23 09:54:24.58495', 'Customer Summary Report', 'Users', 'text-blue-500'),
('5c4e124e-5f07-4c90-b296-bcf82310b492', 'Credit Applications Report', 'تقرير طلبات الائتمان', 'تقرير بجميع طلبات الائتمان وحالاتها', 'credit', 'SELECT * FROM credit_applications', NULL, 'pdf', true, NULL, '2026-07-23 09:54:24.58495', '2026-07-23 09:54:24.58495', 'Credit Applications Report', 'FileText', 'text-green-500'),
('6fabfb5d-0ac4-4eca-9b0d-516e4f7e9759', 'Credit Limits Report', 'تقرير حدود الائتمان', 'تقرير بحدود الائتمان المعتمدة والاستهلاك الحالي', 'credit', 'SELECT * FROM credit_limits', NULL, 'pdf', true, NULL, '2026-07-23 09:54:24.58495', '2026-07-23 09:54:24.58495', 'Credit Limits Report', 'CreditCard', 'text-purple-500'),
('916ee69a-ee44-47f5-bc34-48a5353636db', 'Collections Report', 'تقرير التحصيل', 'تقرير مفصل بالفواتير المتأخرة وأيام التأخير', 'collections', 'SELECT * FROM invoices', NULL, 'pdf', true, NULL, '2026-07-23 09:54:24.58495', '2026-07-23 09:54:24.58495', 'Collections Report', 'TrendingUp', 'text-orange-500'),
('97298c17-d68b-469c-87fb-e275e23e2368', 'Aging Report', 'تقرير التقادم الائتماني', 'تحليل توزيع الديون حسب فترات التأخر', 'collections', 'SELECT * FROM invoices ORDER BY aging_days', NULL, 'pdf', true, NULL, '2026-07-23 09:54:24.58495', '2026-07-23 09:54:24.58495', 'Aging Report', 'BarChart3', 'text-red-500'),
('9b228f95-8293-4b17-8ff9-1709acad3f68', 'Risk Assessment Report', 'تقرير تقييم المخاطر', 'تقييم شامل للمخاطر الائتمانية', 'compliance', 'SELECT * FROM customers', NULL, 'pdf', true, NULL, '2026-07-23 09:54:24.58495', '2026-07-23 09:54:24.58495', 'Risk Assessment Report', 'AlertTriangle', 'text-yellow-500'),
('82733962-53a9-43fc-95e6-be5ef5f8e228', 'Legal Cases Report', 'تقرير القضايا القانونية', 'تقرير بجميع القضايا القانونية الجارية', 'legal', 'SELECT * FROM legal_cases', NULL, 'pdf', true, NULL, '2026-07-23 09:54:24.58495', '2026-07-23 09:54:24.58495', 'Legal Cases Report', 'Scale', 'text-indigo-500'),
('0bdb0525-426f-466f-ac23-372708b70664', 'Document Registry Report', 'تقرير سجل الوثائق', 'تقرير بجميع الوثائق المرفوعة في النظام', 'documents', 'SELECT * FROM documents', NULL, 'pdf', true, NULL, '2026-07-23 09:54:24.58495', '2026-07-23 09:54:24.58495', 'Document Registry Report', 'FolderOpen', 'text-teal-500'),
('4e450b30-a98c-4f66-8e39-08b0dbac939a', 'Audit Trail Report', 'تقرير سجل التدقيق', 'تقرير شامل بجميع العمليات والتعديلات', 'audit', 'SELECT * FROM audit_logs', NULL, 'pdf', true, NULL, '2026-07-23 09:54:24.58495', '2026-07-23 09:54:24.58495', 'Audit Trail Report', 'History', 'text-gray-500');
