import psycopg

conn = psycopg.connect('postgresql://postgres:postgres@localhost:5432/creditai')
conn.autocommit = True
cur = conn.cursor()

cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS approval_status VARCHAR(20) DEFAULT 'pending'")
cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS approved_by UUID")
cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS approved_at TIMESTAMP")
cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS rejection_reason TEXT")
cur.execute("UPDATE users SET approval_status='approved' WHERE is_superuser=true")
cur.execute("UPDATE users SET approval_status='approved' WHERE username='admin'")
print(f'Done: {cur.rowcount} rows updated')
conn.close()
