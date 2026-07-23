--
-- PostgreSQL database dump
--

\restrict X4eAhYkmdigYd5cBCydsSugYiql3eyV4WRL9pgh8wcoyR1N8wnMc2mZUwJjlDYe

-- Dumped from database version 16.13
-- Dumped by pg_dump version 18.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: currencies; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.currencies VALUES ('fb9444bd-8793-4f90-875e-72f422d6885b', 'YER_N', 'Yemeni Rial (North)', 'riyal yamani shamaly', 'YR', true, 1.000000, true, '2026-07-23 10:11:54.925954', '2026-07-23 10:11:54.925954');
INSERT INTO public.currencies VALUES ('4058f587-f9cf-4dfc-8f65-0a3942f5f991', 'SAR', 'Saudi Riyal', 'riyal saudi', 'SR', false, 0.100000, true, '2026-07-23 10:11:54.925954', '2026-07-23 10:11:54.925954');
INSERT INTO public.currencies VALUES ('2a5bfca5-fbec-467e-b339-5f8ef5670f2b', 'USD', 'US Dollar', 'dollar', 'USD', false, 0.004000, true, '2026-07-23 10:11:54.925954', '2026-07-23 10:11:54.925954');
INSERT INTO public.currencies VALUES ('8a7a7655-dd77-4562-a1fc-38724691bc0e', 'EUR', 'Euro', 'يورو', 'EUR', false, 0.003700, false, '2026-07-23 07:16:48.029182', '2026-07-23 07:17:04.91343');
INSERT INTO public.currencies VALUES ('f4c1ddfb-290b-42d2-8ab2-e17240b1ec51', 'YER_S', 'Yemeni Rial (South)', 'riyal yamani januby', 'YR', false, 3.000000, true, '2026-07-23 10:11:54.925954', '2026-07-23 07:30:23.484561');


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.users VALUES ('06e5bbd3-66fc-4df5-8784-cc38447fa31a', 'admin@creditai.com', 'admin', 'System Administrator', 'مسؤول النظام', NULL, '$2b$12$ZWxUzqptHanth1hAncXaIOoB7SjvhEj1PVfGRzXM3nHMcANRtvrk.', NULL, true, true, false, NULL, '2026-07-23 09:25:36.512407', 0, NULL, '{}', '2026-07-23 04:19:44.396993', '2026-07-23 09:25:36.514633');
INSERT INTO public.users VALUES ('4ae91195-2a48-46db-9537-fe2396dd1ce1', 'alimubark@credital.com', 'ali', 'ali mubark', 'علي مبارك', NULL, '$2b$12$ahA0yBy4aGyDyP17DhizDu0jV0OBqAyXXITD6pmHsj/gvV7rslluK', NULL, true, false, false, NULL, '2026-07-23 07:37:20.294276', 0, NULL, '{}', '2026-07-23 05:40:10.882149', '2026-07-23 07:37:20.296338');


--
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.customers VALUES ('26c52450-7077-4055-b8fc-5ae681abadb9', '5aea2896-dfea-42f4-ae00-09e4580debc9', 'CUST-00001', 'Test Customer', '???? ??????', NULL, 'retail', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'active', 'not_started', 'not_verified', NULL, NULL, '{}', true, '2026-07-23 05:51:22.34331', '2026-07-23 05:51:22.343313', '06e5bbd3-66fc-4df5-8784-cc38447fa31a', NULL);
INSERT INTO public.customers VALUES ('8c92ee1c-77ea-4165-ae3a-72a35c68dcf0', '5aea2896-dfea-42f4-ae00-09e4580debc9', 'CUST-00003', 'Test', 'test', NULL, 'retail', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'active', 'not_started', 'not_verified', NULL, NULL, '{}', true, '2026-07-23 05:52:27.98702', '2026-07-23 05:52:27.987023', '06e5bbd3-66fc-4df5-8784-cc38447fa31a', NULL);
INSERT INTO public.customers VALUES ('e5ceff14-38c7-4610-b06d-530c3323c6e2', '5aea2896-dfea-42f4-ae00-09e4580debc9', 'CUST-00004', 'Test Customer', '???? ??????', NULL, 'retail', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'active', 'not_started', 'not_verified', NULL, NULL, '{}', true, '2026-07-23 05:53:24.05221', '2026-07-23 05:53:24.052214', '06e5bbd3-66fc-4df5-8784-cc38447fa31a', NULL);
INSERT INTO public.customers VALUES ('4834743a-bfc3-405c-81f7-4c743fb24882', '5aea2896-dfea-42f4-ae00-09e4580debc9', 'CUST-00005', 'Test Customer', '???? ??????', NULL, 'retail', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'active', 'not_started', 'not_verified', NULL, NULL, '{}', true, '2026-07-23 05:53:53.835824', '2026-07-23 05:53:53.835827', '06e5bbd3-66fc-4df5-8784-cc38447fa31a', NULL);
INSERT INTO public.customers VALUES ('7ea89fd2-e92f-4e2c-88ac-9bf089d5bd68', '5aea2896-dfea-42f4-ae00-09e4580debc9', 'CUST-00006', 'Test', 'test', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'pending', 'not_started', 'not_verified', NULL, NULL, '{}', true, '2026-07-23 05:54:26.389584', '2026-07-23 05:54:26.389591', '06e5bbd3-66fc-4df5-8784-cc38447fa31a', NULL);
INSERT INTO public.customers VALUES ('051d754b-c1a6-48ac-8b40-c49ac9117000', '5aea2896-dfea-42f4-ae00-09e4580debc9', 'CUST-00007', 'Test Customer', '???? ??????', NULL, 'retail', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'active', 'not_started', 'not_verified', NULL, NULL, NULL, true, '2026-07-23 05:58:05.438932', '2026-07-23 05:58:05.438935', '06e5bbd3-66fc-4df5-8784-cc38447fa31a', NULL);
INSERT INTO public.customers VALUES ('537815f3-5e3c-4245-af6b-1ef3baa07b42', '5aea2896-dfea-42f4-ae00-09e4580debc9', 'CUST-00002', 'alghith systemes', 'الغيث للانظمة', 'alghith systemes', 'trading', 'platinum', '', '', NULL, '0555454', '0154544', NULL, 'active', 'not_started', 'not_verified', NULL, NULL, '{}', true, '2026-07-23 05:51:36.256652', '2026-07-23 08:32:21.455427', '06e5bbd3-66fc-4df5-8784-cc38447fa31a', '06e5bbd3-66fc-4df5-8784-cc38447fa31a');


--
-- Data for Name: credit_applications; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.credit_applications VALUES ('a5616e3f-dbf5-4809-8295-acfa19c24d62', '537815f3-5e3c-4245-af6b-1ef3baa07b42', 'guarantee', 5000000.00, 'fb9444bd-8793-4f90-875e-72f422d6885b', 'شراء بضاعة', 'draft', '06e5bbd3-66fc-4df5-8784-cc38447fa31a', NULL, NULL, NULL, NULL, NULL, NULL, '[]', NULL, true, '2026-07-23 06:43:52.315747', '2026-07-23 07:31:14.003031');
INSERT INTO public.credit_applications VALUES ('7daaa51b-edc5-46a9-889d-fcbfc45df629', '537815f3-5e3c-4245-af6b-1ef3baa07b42', 'loan', 1000000.00, 'fb9444bd-8793-4f90-875e-72f422d6885b', 'شراء بضاعة', 'draft', '06e5bbd3-66fc-4df5-8784-cc38447fa31a', NULL, NULL, NULL, NULL, NULL, NULL, '[]', NULL, true, '2026-07-23 07:31:55.744655', '2026-07-23 07:31:55.744658');


--
-- Data for Name: credit_limits; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.credit_limits VALUES ('a19ef19a-78ae-4948-8d21-97c316d55af6', '537815f3-5e3c-4245-af6b-1ef3baa07b42', 'guarantee', 1000000.00, 'fb9444bd-8793-4f90-875e-72f422d6885b', 0.00, 1000000.00, 0.00, '2026-01-01 00:00:00', '2026-06-30 00:00:00', 'active', '06e5bbd3-66fc-4df5-8784-cc38447fa31a', NULL, NULL, true, '2026-07-23 08:41:29.691929', '2026-07-23 08:41:29.691933');


--
-- Data for Name: permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: report_templates; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.report_templates VALUES ('d08e4b96-2055-4049-823f-ad7bc3596abe', 'Customer Summary Report', 'تقرير ملخص العملاء', 'تقرير شامل يحتوي على ملخص لجميع العملاء وبياناتهم الأساسية', 'customers', 'SELECT * FROM customers', NULL, 'pdf', true, NULL, '2026-07-23 09:54:24.58495', '2026-07-23 09:54:24.58495', 'Customer Summary Report', 'Users', 'text-blue-500');
INSERT INTO public.report_templates VALUES ('5c4e124e-5f07-4c90-b296-bcf82310b492', 'Credit Applications Report', 'تقرير طلبات الائتمان', 'تقرير بجميع طلبات الائتمان وحالاتها', 'credit', 'SELECT * FROM credit_applications', NULL, 'pdf', true, NULL, '2026-07-23 09:54:24.58495', '2026-07-23 09:54:24.58495', 'Credit Applications Report', 'FileText', 'text-green-500');
INSERT INTO public.report_templates VALUES ('6fabfb5d-0ac4-4eca-9b0d-516e4f7e9759', 'Credit Limits Report', 'تقرير حدود الائتمان', 'تقرير بحدود الائتمان المعتمدة والاستهلاك الحالي', 'credit', 'SELECT * FROM credit_limits', NULL, 'pdf', true, NULL, '2026-07-23 09:54:24.58495', '2026-07-23 09:54:24.58495', 'Credit Limits Report', 'CreditCard', 'text-purple-500');
INSERT INTO public.report_templates VALUES ('916ee69a-ee44-47f5-bc34-48a5353636db', 'Collections Report', 'تقرير التحصيل', 'تقرير مفصل بالفواتير المتأخرة وأيام التأخير', 'collections', 'SELECT * FROM invoices', NULL, 'pdf', true, NULL, '2026-07-23 09:54:24.58495', '2026-07-23 09:54:24.58495', 'Collections Report', 'TrendingUp', 'text-orange-500');
INSERT INTO public.report_templates VALUES ('97298c17-d68b-469c-87fb-e275e23e2368', 'Aging Report', 'تقرير التقادم الائتماني', 'تحليل توزيع الديون حسب فترات التأخر', 'collections', 'SELECT * FROM invoices ORDER BY aging_days', NULL, 'pdf', true, NULL, '2026-07-23 09:54:24.58495', '2026-07-23 09:54:24.58495', 'Aging Report', 'BarChart3', 'text-red-500');
INSERT INTO public.report_templates VALUES ('9b228f95-8293-4b17-8ff9-1709acad3f68', 'Risk Assessment Report', 'تقرير تقييم المخاطر', 'تقييم شامل للمخاطر الائتمانية', 'compliance', 'SELECT * FROM customers', NULL, 'pdf', true, NULL, '2026-07-23 09:54:24.58495', '2026-07-23 09:54:24.58495', 'Risk Assessment Report', 'AlertTriangle', 'text-yellow-500');
INSERT INTO public.report_templates VALUES ('82733962-53a9-43fc-95e6-be5ef5f8e228', 'Legal Cases Report', 'تقرير القضايا القانونية', 'تقرير بجميع القضايا القانونية الجارية', 'legal', 'SELECT * FROM legal_cases', NULL, 'pdf', true, NULL, '2026-07-23 09:54:24.58495', '2026-07-23 09:54:24.58495', 'Legal Cases Report', 'Scale', 'text-indigo-500');
INSERT INTO public.report_templates VALUES ('0bdb0525-426f-466f-ac23-372708b70664', 'Document Registry Report', 'تقرير سجل الوثائق', 'تقرير بجميع الوثائق المرفوعة في النظام', 'documents', 'SELECT * FROM documents', NULL, 'pdf', true, NULL, '2026-07-23 09:54:24.58495', '2026-07-23 09:54:24.58495', 'Document Registry Report', 'FolderOpen', 'text-teal-500');
INSERT INTO public.report_templates VALUES ('4e450b30-a98c-4f66-8e39-08b0dbac939a', 'Audit Trail Report', 'تقرير سجل التدقيق', 'تقرير شامل بجميع العمليات والتعديلات', 'audit', 'SELECT * FROM audit_logs', NULL, 'pdf', true, NULL, '2026-07-23 09:54:24.58495', '2026-07-23 09:54:24.58495', 'Audit Trail Report', 'History', 'text-gray-500');


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.roles VALUES ('53cab030-9c48-4c7b-9f4f-0d0ee7196123', 'Super Admin', 'مسؤول النظام', 'Full system access', true, '["*"]', true, '2026-07-23 04:19:44.075628', '2026-07-23 04:19:44.075633');
INSERT INTO public.roles VALUES ('25b3da7a-8598-46ba-ae1c-5a2075e79356', 'مسؤول عن العملاء', 'مسؤول عن العملاء', 'يضيف ويعدل فيما يخص العملاء', false, '["customers:read", "customers:create", "customers:update", "customers:delete", "customers:export", "collections:read", "collections:create", "collections:update", "collections:delete", "collections:assign", "collections:export", "documents:read", "documents:create", "documents:update", "documents:upload", "documents:ocr", "documents:export", "reports:read", "reports:create", "reports:execute", "reports:export", "sales:read", "sales:create", "sales:update", "sales:delete", "sales:import", "sales:export"]', true, '2026-07-23 05:42:41.178436', '2026-07-23 07:59:05.486428');


--
-- Data for Name: sales_invoices; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.sales_invoices VALUES ('ddd18ff9-b10f-4b92-8f10-42b5e7036a0a', '0001', '537815f3-5e3c-4245-af6b-1ef3baa07b42', '2026-06-22 00:00:00', '2026-07-21 00:00:00', 20000000.00, 0.00, 0.00, 20000000.00, 0.00, 20000000.00, 'fb9444bd-8793-4f90-875e-72f422d6885b', 'draft', NULL, NULL, '[]', NULL, true, '2026-07-23 07:50:56.753095', '2026-07-23 07:50:56.753099', 'سكر', 50.00);


--
-- Data for Name: user_roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.user_roles VALUES ('06e5bbd3-66fc-4df5-8784-cc38447fa31a', '53cab030-9c48-4c7b-9f4f-0d0ee7196123', '2026-07-23 04:19:44.402556');
INSERT INTO public.user_roles VALUES ('4ae91195-2a48-46db-9537-fe2396dd1ce1', '25b3da7a-8598-46ba-ae1c-5a2075e79356', '2026-07-23 08:08:09.3046');


--
-- PostgreSQL database dump complete
--

\unrestrict X4eAhYkmdigYd5cBCydsSugYiql3eyV4WRL9pgh8wcoyR1N8wnMc2mZUwJjlDYe

