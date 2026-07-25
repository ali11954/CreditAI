"""
Full Order-to-Cash Test Data Seed — LOCAL ONLY
"""
import psycopg
import uuid
from datetime import datetime, timedelta

DB_URL = "postgresql://postgres:postgres@localhost:5432/creditai"

def uid(): return str(uuid.uuid4())
def days_ago(n): return datetime.utcnow() - timedelta(days=n)
def days_from_now(n): return datetime.utcnow() + timedelta(days=n)

def seed():
    conn = psycopg.connect(DB_URL)
    conn.autocommit = True
    cur = conn.cursor()

    company_id = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    admin_id = "06e5bbd3-66fc-4df5-8784-cc38447fa31a"

    # Company
    cur.execute("SELECT id FROM companies WHERE id = %s", (company_id,))
    if not cur.fetchone():
        cur.execute("INSERT INTO companies (id, name, name_ar, registration_number, is_active, created_at, updated_at) VALUES (%s, 'CreditAI Corp', 'شركة كريديت أي آي', 'CR-001', true, now(), now())", (company_id,))
    print("[1] Company OK")

    # Currencies
    yer_id = usd_id = None
    for code, name, name_ar, rate, is_base in [("YER_N", "Yemeni Rial", "ريال يمني", 1.0, True), ("USD", "US Dollar", "دولار", 0.004, False), ("SAR", "Saudi Riyal", "ريال سعودي", 0.1, False)]:
        cur.execute("SELECT id FROM currencies WHERE code = %s", (code,))
        row = cur.fetchone()
        if row:
            if code == "YER_N": yer_id = row[0]
            if code == "USD": usd_id = row[0]
            continue
        cid = uid()
        cur.execute("INSERT INTO currencies (id, code, name, name_ar, symbol, is_base, exchange_rate, is_active, created_at, updated_at) VALUES (%s, %s, %s, %s, '﷼', %s, %s, true, now(), now())", (cid, code, name, name_ar, is_base, rate))
        if code == "YER_N": yer_id = cid
        if code == "USD": usd_id = cid
    print("[2] Currencies OK")

    # Roles
    role_id = "53cab030-9c48-4c7b-9f4f-0d0ee7196123"
    cur.execute("SELECT id FROM roles WHERE id = %s", (role_id,))
    if not cur.fetchone():
        cur.execute("INSERT INTO roles (id, name, name_ar, description, is_system, permissions, is_active, created_at, updated_at) VALUES (%s, 'Super Admin', 'مسؤول النظام', 'Full access', true, '[\"*\"]'::jsonb, true, now(), now())", (role_id,))
    cur.execute("SELECT 1 FROM user_roles WHERE user_id = %s AND role_id = %s", (admin_id, role_id))
    if not cur.fetchone():
        cur.execute("INSERT INTO user_roles (user_id, role_id, assigned_at) VALUES (%s, %s, now())", (admin_id, role_id))
    print("[3] Roles OK")

    # === CUSTOMERS ===
    customers = [
        ("C-001", "Al-Noor Trading Co.", "شركة النور للتجارة", "Trading", "gold", "low", 85, "active", "Sana'a"),
        ("C-002", "Yemen Gulf Construction", "شركة الخليج اليمنية للمقاولات", "Construction", "platinum", "low", 92, "active", "Aden"),
        ("C-003", "Al-Baraka Foods", "شركة البركة للأغذية", "Food & Beverage", "silver", "medium", 68, "active", "Taiz"),
        ("C-004", "Hadramout Oil & Gas", "شركة حضرموت للنفط والغاز", "Oil & Gas", "platinum", "low", 95, "active", "Hadramout"),
        ("C-005", "Saba Tech Solutions", "سبأ للحلول التقنية", "Technology", "gold", "medium", 75, "active", "Sana'a"),
        ("C-006", "Red Sea Hotels Group", "مجموعة فنادق البحر الأحمر", "Hospitality", "silver", "medium", 70, "active", "Hodeidah"),
        ("C-007", "Al-Thawra Agricultural", "شركة الثورة الزراعية", "Agriculture", "bronze", "high", 45, "active", "Ibb"),
        ("C-008", "Future Pharma Yemen", "فيوتشر فارما اليمن", "Pharmaceutical", "gold", "low", 88, "active", "Sana'a"),
        ("C-009", "National Logistics Co.", "شركة الناشونال للخدمات اللوجستية", "Logistics", "standard", "high", 35, "active", "Aden"),
        ("C-010", "Smart City Developers", "مطوري المدينة الذكية", "Real Estate", "silver", "medium", 62, "active", "Sana'a"),
    ]
    cids = {}
    for code, name, name_ar, btype, classification, risk, score, status, region in customers:
        cur.execute("SELECT id FROM customers WHERE customer_code = %s", (code,))
        row = cur.fetchone()
        if row:
            cids[code] = row[0]; continue
        cid = uid(); cids[code] = cid
        cur.execute("""INSERT INTO customers (id, company_id, customer_code, name, name_ar, business_type, classification, risk_category, credit_score, status, sales_region, onboarding_status, kyc_status, is_active, created_by, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'completed', 'verified', true, %s, now(), now())""",
            (cid, company_id, code, name, name_ar, btype, classification, risk, score, status, region, admin_id))
    print("[4] 10 Customers OK")

    # === CREDIT APPLICATIONS ===
    apps = [
        ("C-001", 5000000, "approved", "Low risk - established trading company"),
        ("C-002", 15000000, "approved", "Platinum - large construction projects"),
        ("C-003", 2000000, "pending", "Medium risk - food industry"),
        ("C-004", 25000000, "approved", "Top tier - oil & gas, government backed"),
        ("C-005", 3000000, "approved", "Technology company, growing"),
        ("C-007", 800000, "rejected", "High risk - seasonal income"),
        ("C-008", 8000000, "approved", "Pharmaceutical distributor"),
        ("C-010", 4000000, "pending", "Real estate developer"),
    ]
    app_ids = {}
    for i, (code, amount, status, notes) in enumerate(apps):
        cid = cids[code]
        cur.execute("SELECT id FROM credit_applications WHERE customer_id = %s ORDER BY created_at DESC LIMIT 1", (cid,))
        row = cur.fetchone()
        if row: app_ids[code] = row[0]; continue
        aid = uid(); app_ids[code] = aid
        cur.execute("""INSERT INTO credit_applications (id, customer_id, application_type, requested_amount, currency_id, purpose, status, submitted_by, submitted_at, notes, is_active, created_at, updated_at)
            VALUES (%s, %s, 'credit_limit', %s, %s, 'Working capital', %s, %s, %s, %s, true, now(), now())""",
            (aid, cid, amount, yer_id, status, admin_id, days_ago(90 - i*10), notes))
    print("[5] 8 Credit Applications OK")

    # Credit analyses
    for code, aid in app_ids.items():
        cur.execute("SELECT 1 FROM credit_analyses WHERE application_id = %s", (aid,))
        if cur.fetchone(): continue
        cur.execute("""INSERT INTO credit_analyses (id, application_id, customer_id, analysis_type, financial_data, ratios, cash_flow, risk_rating, credit_score, ai_recommendation, analyst_id, analyst_notes, analyzed_at, is_active, created_at, updated_at)
            VALUES (%s, %s, %s, 'comprehensive', '{"revenue": 10000000, "profit": 1500000}'::jsonb, '{"debt_to_equity": 1.2, "liquidity": 1.8}'::jsonb, '{"operating": 2000000}'::jsonb, 'low', 85, 'Approve - strong financial position', %s, 'Reviewed and approved', now(), true, now(), now())""",
            (uid(), aid, cids[code], admin_id))
    print("[6] Credit Analyses OK")

    # Credit limits
    for code, amount in [("C-001", 5000000), ("C-002", 15000000), ("C-004", 25000000), ("C-005", 3000000), ("C-008", 8000000)]:
        cid = cids[code]
        cur.execute("SELECT id FROM credit_limits WHERE customer_id = %s", (cid,))
        if cur.fetchone(): continue
        cur.execute("""INSERT INTO credit_limits (id, customer_id, limit_type, amount, currency_id, utilized_amount, available_amount, reserved_amount, start_date, end_date, status, approved_by, is_active, created_at, updated_at)
            VALUES (%s, %s, 'total', %s, %s, 0, %s, 0, %s, %s, 'active', %s, true, now(), now())""",
            (uid(), cid, amount, yer_id, amount, days_ago(365), days_from_now(365), admin_id))
    print("[7] Credit Limits OK")

    # === SALES INVOICES ===
    invs = [
        ("C-001", "SI-2024-001", 2500000, 2500000, days_ago(60), days_ago(30), "paid"),
        ("C-001", "SI-2024-002", 1800000, 0, days_ago(45), days_from_now(15), "pending"),
        ("C-001", "SI-2024-003", 3200000, 1000000, days_ago(20), days_from_now(40), "partial"),
        ("C-002", "SI-2024-004", 7500000, 7500000, days_ago(90), days_ago(60), "paid"),
        ("C-002", "SI-2024-005", 5000000, 0, days_ago(30), days_from_now(30), "pending"),
        ("C-003", "SI-2024-006", 800000, 200000, days_ago(75), days_ago(15), "overdue"),
        ("C-003", "SI-2024-007", 1200000, 0, days_ago(10), days_from_now(50), "pending"),
        ("C-004", "SI-2024-008", 12000000, 12000000, days_ago(120), days_ago(90), "paid"),
        ("C-004", "SI-2024-009", 8500000, 3000000, days_ago(40), days_from_now(20), "partial"),
        ("C-005", "SI-2024-010", 1500000, 0, days_ago(50), days_ago(10), "overdue"),
        ("C-005", "SI-2024-011", 2200000, 2200000, days_ago(30), days_ago(10), "paid"),
        ("C-007", "SI-2024-012", 500000, 0, days_ago(100), days_ago(40), "overdue"),
        ("C-008", "SI-2024-013", 4000000, 4000000, days_ago(60), days_ago(30), "paid"),
        ("C-008", "SI-2024-014", 3500000, 1500000, days_ago(25), days_from_now(35), "partial"),
        ("C-009", "SI-2024-015", 600000, 0, days_ago(110), days_ago(50), "overdue"),
        ("C-010", "SI-2024-016", 2800000, 0, days_ago(15), days_from_now(45), "pending"),
        ("C-001", "SI-2024-017", 1500000, 500000, days_ago(5), days_from_now(55), "partial"),
        ("C-002", "SI-2024-018", 3000000, 3000000, days_ago(15), days_ago(5), "paid"),
    ]
    inv_ids = {}
    for code, inv_num, amount, paid, inv_date, due_date, status in invs:
        cur.execute("SELECT id FROM sales_invoices WHERE invoice_number = %s", (inv_num,))
        row = cur.fetchone()
        if row: inv_ids[inv_num] = row[0]; continue
        iid = uid(); inv_ids[inv_num] = iid
        balance = amount - paid
        cur.execute("""INSERT INTO sales_invoices (id, invoice_number, customer_id, invoice_date, due_date, amount, tax_amount, discount_amount, total_amount, paid_amount, balance, currency_id, status, payment_terms, is_active, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, 0, 0, %s, %s, %s, %s, %s, 'Net 60', true, now(), now())""",
            (iid, inv_num, cids[code], inv_date, due_date, amount, amount, paid, balance, yer_id, status))
    print("[8] 18 Sales Invoices OK")

    # === COLLECTION INVOICES (linked to sales) ===
    coll_count = 0
    for inv_num, iid in inv_ids.items():
        cur.execute("SELECT id FROM invoices WHERE invoice_number = %s", (inv_num,))
        if cur.fetchone(): continue
        cur.execute("SELECT customer_id, total_amount, paid_amount, balance, status, due_date FROM sales_invoices WHERE id = %s", (iid,))
        row = cur.fetchone()
        if not row: continue
        cid, total, paid, bal, status, due = row
        aging = max(0, (datetime.utcnow() - due).days if due < datetime.utcnow() else 0)
        coll_status = "paid" if status == "paid" else ("overdue" if aging > 0 else "pending")
        cur.execute("""INSERT INTO invoices (id, customer_id, invoice_number, invoice_date, due_date, amount, paid_amount, balance, currency_id, status, aging_days, sales_invoice_id, is_active, created_at, updated_at)
            VALUES (%s, %s, %s, now(), %s, %s, %s, %s, %s, %s, %s, %s, true, now(), now())""",
            (uid(), cid, inv_num, due, total, paid, bal, yer_id, coll_status, aging, iid))
        coll_count += 1
    print(f"[9] {coll_count} Collection Invoices OK")

    # === COLLECTION ACTIVITIES ===
    acts = [
        ("C-001", "phone_call", "Initial contact for overdue payment", "Customer acknowledged the debt"),
        ("C-001", "email", "Sent payment reminder for SI-2024-003", "Awaiting response"),
        ("C-003", "phone_call", "Follow up on SI-2024-006 overdue", "Customer requested extension"),
        ("C-003", "visit", "On-site visit to discuss payment plan", "Customer agreed to pay 50% this week"),
        ("C-005", "email", "Sent overdue notice for SI-2024-010", "No response"),
        ("C-005", "phone_call", "Second follow-up call", "Customer experiencing cash flow issues"),
        ("C-007", "phone_call", "Called regarding SI-2024-012", "Customer requested 30-day extension"),
        ("C-009", "email", "Final notice before legal action", "Customer non-responsive"),
    ]
    for code, atype, subject, outcome in acts:
        cid = cids[code]
        cur.execute("SELECT 1 FROM collection_activities WHERE customer_id = %s AND subject = %s", (cid, subject))
        if cur.fetchone(): continue
        cur.execute("""INSERT INTO collection_activities (id, customer_id, activity_type, direction, subject, content, outcome, created_by, is_active, created_at, updated_at)
            VALUES (%s, %s, %s, 'outbound', %s, %s, %s, %s, true, now(), now())""",
            (uid(), cid, atype, subject, subject, outcome, admin_id))
    print("[10] Collection Activities OK")

    # === PROMISES TO PAY ===
    promises = [
        ("C-001", days_ago(5), 3200000, "fulfilled"),
        ("C-003", days_from_now(7), 600000, "pending"),
        ("C-005", days_from_now(14), 1500000, "pending"),
        ("C-007", days_from_now(30), 500000, "pending"),
        ("C-009", days_ago(20), 600000, "broken"),
    ]
    for code, pdate, amount, status in promises:
        cid = cids[code]
        cur.execute("SELECT 1 FROM promises_to_pay WHERE customer_id = %s AND amount = %s", (cid, amount))
        if cur.fetchone(): continue
        cur.execute("""INSERT INTO promises_to_pay (id, customer_id, promise_date, amount, status, notes, created_by, is_active, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, 'Test data', %s, true, now(), now())""",
            (uid(), cid, pdate, amount, status, admin_id))
    print("[11] Promises to Pay OK")

    # === INSTALLMENT PLAN ===
    cur.execute("SELECT 1 FROM installment_plans WHERE customer_id = %s", (cids["C-003"],))
    if not cur.fetchone():
        pid = uid()
        cur.execute("""INSERT INTO installment_plans (id, customer_id, total_amount, down_payment, number_of_installments, frequency, status, approved_by, is_active, created_at, updated_at)
            VALUES (%s, %s, 1200000, 200000, 5, 'monthly', 'active', %s, true, now(), now())""", (pid, cids["C-003"], admin_id))
        for i in range(1, 6):
            cur.execute("""INSERT INTO installments (id, plan_id, installment_number, due_date, amount, paid_amount, status, is_active, created_at, updated_at)
                VALUES (%s, %s, %s, %s, 200000, %s, %s, true, now(), now())""",
                (uid(), pid, i, days_from_now(i*30), 200000 if i <= 2 else 0, "paid" if i <= 2 else "pending"))
    print("[12] Installment Plan OK")

    # === SETTLEMENT ===
    cur.execute("SELECT 1 FROM settlements WHERE customer_id = %s", (cids["C-009"],))
    if not cur.fetchone():
        cur.execute("""INSERT INTO settlements (id, customer_id, original_amount, settled_amount, discount_percentage, discount_amount, settlement_date, approved_by, reason, is_active, created_at, updated_at)
            VALUES (%s, %s, 600000, 450000, 25.0, 150000, now(), %s, 'Settlement to close overdue account', true, now(), now())""",
            (uid(), cids["C-009"], admin_id))
    print("[13] Settlement OK")

    # === LAWYERS ===
    lawyer_ids = []
    for name, firm, spec in [("Dr. Ahmed Al-Hakimi", "Al-Hakimi Law Firm", "Commercial Law"), ("Dr. Fatima Al-Sayaghi", "Sayaghi & Partners", "Debt Recovery")]:
        cur.execute("SELECT id FROM lawyers WHERE name = %s", (name,))
        row = cur.fetchone()
        if row: lawyer_ids.append(row[0]); continue
        lid = uid(); lawyer_ids.append(lid)
        cur.execute("""INSERT INTO lawyers (id, name, firm_name, phone, email, specialization, license_number, is_active, created_at, updated_at)
            VALUES (%s, %s, %s, '+967-777-123456', 'law@example.com', %s, 'LY-2020-0456', true, now(), now())""",
            (lid, name, firm, spec))
    print("[14] Lawyers OK")

    # === LEGAL CASE ===
    cur.execute("SELECT 1 FROM legal_cases WHERE is_active = true LIMIT 1")
    if not cur.fetchone():
        case_id = uid()
        cur.execute("""INSERT INTO legal_cases (id, customer_id, case_number, case_type, court_name, filing_date, status, amount_in_dispute, currency_id, assigned_lawyer_id, notes, is_active, created_by, created_at, updated_at)
            VALUES (%s, %s, 'LC-2024-001', 'Debt Recovery', 'Sana''a Commercial Court', %s, 'open', 500000, %s, %s, 'Overdue invoice SI-2024-012', true, %s, now(), now())""",
            (case_id, cids["C-007"], days_ago(30), yer_id, lawyer_ids[1] if len(lawyer_ids) > 1 else lawyer_ids[0], admin_id))
        cur.execute("""INSERT INTO court_hearings (id, case_id, hearing_date, judge, outcome, notes, is_active, created_at, updated_at)
            VALUES (%s, %s, %s, 'Judge Mohammed Al-Aghbari', 'First hearing - case accepted', 'Documents submitted', true, now(), now())""",
            (uid(), case_id, days_from_now(14)))
        for etype, desc, edate in [("filing", "Case filed", days_ago(30)), ("assignment", "Assigned to lawyer", days_ago(28)), ("notification", "Defendant notified", days_ago(20))]:
            cur.execute("""INSERT INTO legal_timelines (id, case_id, event_date, event_type, description, created_by, is_active, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, true, now(), now())""",
                (uid(), case_id, edate, etype, desc, admin_id))
    print("[15] Legal Case + Hearings + Timeline OK")

    # === GUARANTORS ===
    for code, gname in [("C-003", "Mohammed Al-Bahr"), ("C-007", "Ali Al-Mutawakil")]:
        cid = cids[code]
        cur.execute("SELECT 1 FROM guarantors WHERE customer_id = %s", (cid,))
        if cur.fetchone(): continue
        cur.execute("""INSERT INTO guarantors (id, customer_id, name, relationship_type, guarantor_type, is_individual, phone, email, status, is_active, created_at, updated_at)
            VALUES (%s, %s, %s, 'business_partner', 'corporate', false, '+967-777-888888', 'guarantor@example.com', 'active', true, now(), now())""",
            (uid(), cid, gname))
    print("[16] Guarantors OK")

    # === COLLATERAL ===
    for code, ctype, desc, value in [("C-003", "real_estate", "Commercial warehouse in Taiz", 3000000), ("C-007", "vehicle", "Toyota Hilux 2022", 1200000)]:
        cid = cids[code]
        cur.execute("SELECT 1 FROM collaterals WHERE customer_id = %s", (cid,))
        if cur.fetchone(): continue
        cur.execute("""INSERT INTO collaterals (id, customer_id, type, description, estimated_value, currency_id, status, insurance_required, is_active, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, 'verified', true, true, now(), now())""",
            (uid(), cid, ctype, desc, value, yer_id))
    print("[17] Collateral OK")

    # === KYC ===
    for code in ["C-001", "C-002", "C-004", "C-008"]:
        cid = cids[code]
        cur.execute("SELECT 1 FROM kyc_records WHERE customer_id = %s", (cid,))
        if cur.fetchone(): continue
        cur.execute("""INSERT INTO kyc_records (id, customer_id, type, status, verified_by, verified_at, expires_at, is_active, created_at, updated_at)
            VALUES (%s, %s, 'commercial_registration', 'verified', %s, now(), %s, true, now(), now())""",
            (uid(), cid, admin_id, days_from_now(365)))
    print("[18] KYC OK")

    # === AML ===
    for code in ["C-004", "C-002"]:
        cid = cids[code]
        cur.execute("SELECT 1 FROM aml_checks WHERE customer_id = %s", (cid,))
        if cur.fetchone(): continue
        cur.execute("""INSERT INTO aml_checks (id, customer_id, check_type, result, score, details, checked_at, checked_by, is_active)
            VALUES (%s, %s, 'screening', 'clear', 95, '{"result": "clear"}'::jsonb, now(), %s, true)""",
            (uid(), cid, admin_id))
    print("[19] AML OK")

    # === INSURANCE ===
    cur.execute("SELECT 1 FROM insurance_companies WHERE is_active = true LIMIT 1")
    if not cur.fetchone():
        icid = uid()
        cur.execute("""INSERT INTO insurance_companies (id, name, name_ar, license_number, phone, email, is_active, created_at, updated_at)
            VALUES (%s, 'Yemen General Insurance', 'التأمين العام اليمني', 'INS-2019-001', '+967-1-234567', 'info@ygi.com', true, now(), now())""", (icid,))
        for code in ["C-001", "C-002"]:
            cid = cids[code]
            cur.execute("SELECT 1 FROM insurance_policies WHERE customer_id = %s", (cid,))
            if cur.fetchone(): continue
            cur.execute("""INSERT INTO insurance_policies (id, customer_id, insurance_company_id, policy_number, policy_type, coverage_amount, premium, start_date, end_date, status, is_active, created_at, updated_at)
                VALUES (%s, %s, %s, 'POL-2024-' || %s, 'credit_insurance', 5000000, 50000, '2024-01-01', '2024-12-31', 'active', true, now(), now())""",
                (uid(), cid, icid, code[-3:]))
    print("[20] Insurance OK")

    # === EXPOSURE ===
    for code in ["C-001", "C-002", "C-004"]:
        cid = cids[code]
        cur.execute("SELECT 1 FROM exposures WHERE customer_id = %s", (cid,))
        if cur.fetchone(): continue
        cur.execute("""INSERT INTO exposures (id, customer_id, exposure_type, amount, currency_id, calculated_at, is_active, created_at, updated_at)
            VALUES (%s, %s, 'credit', %s, %s, now(), true, now(), now())""",
            (uid(), cid, 5000000, yer_id))
    print("[21] Exposure OK")

    # === COMMUNICATION TEMPLATES ===
    cur.execute("SELECT 1 FROM communication_templates WHERE is_active = true LIMIT 1")
    if not cur.fetchone():
        for name, name_ar, ttype, body in [("Payment Reminder", "تذكير بالدفع", "payment_reminder", "Dear {customer_name}, please pay invoice {invoice_number}."), ("Overdue Notice", "إشعار تأخر", "overdue", "Your invoice {invoice_number} is overdue."), ("Welcome", "ترحيب", "welcome", "Welcome to CreditAI.")]:
            cur.execute("""INSERT INTO communication_templates (id, name, name_ar, type, body, is_active, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, true, now(), now())""", (uid(), name, name_ar, ttype, body))
    print("[22] Communication Templates OK")

    # === WORKFLOW TEMPLATES ===
    cur.execute("SELECT 1 FROM workflow_templates WHERE is_active = true LIMIT 1")
    if not cur.fetchone():
        for name, module, steps in [("Credit Approval", "credit", '[{"name":"Analyst Review"},{"name":"Manager Approval"}]'), ("Invoice Approval", "invoicing", '[{"name":"Sales Review"},{"name":"Finance Approval"}]')]:
            cur.execute("""INSERT INTO workflow_templates (id, name, description, module, is_active, steps, created_at, updated_at)
                VALUES (%s, %s, %s, %s, true, %s::jsonb, now(), now())""", (uid(), name, f"{name} workflow", module, steps))
    print("[23] Workflow Templates OK")

    # === DOCUMENT FOLDERS ===
    cur.execute("SELECT 1 FROM document_folders WHERE is_active = true LIMIT 1")
    if not cur.fetchone():
        for name in ["Credit Applications", "Invoices", "Legal Documents", "Customer Documents"]:
            cur.execute("""INSERT INTO document_folders (id, name, company_id, is_shared, created_by, is_active, created_at, updated_at)
                VALUES (%s, %s, %s, true, %s, true, now(), now())""", (uid(), name, company_id, admin_id))
    print("[24] Document Folders OK")

    # === NOTIFICATIONS ===
    for title, title_ar, ntype in [("New Credit Application", "طلب ائتمان جديد", "info"), ("Invoice Overdue", "فاتورة متأخرة", "warning"), ("Payment Received", "تم استلام الدفع", "success")]:
        cur.execute("SELECT 1 FROM notifications WHERE user_id = %s AND title = %s", (admin_id, title))
        if cur.fetchone(): continue
        cur.execute("""INSERT INTO notifications (id, user_id, title, title_ar, message, message_ar, type, is_read, is_active, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, false, true, now(), now())""",
            (uid(), admin_id, title, title_ar, f"Test: {title}", f"تجريبي: {title_ar}", ntype))
    print("[25] Notifications OK")

    # === SUMMARY ===
    print("\n" + "=" * 60)
    print("SEED COMPLETE!")
    print("=" * 60)
    for table in ["customers","credit_applications","credit_analyses","credit_limits","sales_invoices","invoices","collection_activities","promises_to_pay","installment_plans","installments","settlements","legal_cases","court_hearings","legal_timelines","guarantors","collaterals","kyc_records","aml_checks","insurance_companies","insurance_policies","exposures","communication_templates","workflow_templates","document_folders","notifications"]:
        try:
            cur.execute(f"SELECT count(*) FROM {table}")
            print(f"  {table}: {cur.fetchone()[0]}")
        except: pass

    conn.close()
    print("\nLogin: admin@creditai.com / Admin@123")

if __name__ == "__main__":
    seed()
