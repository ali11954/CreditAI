import psycopg
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

# ============================================================
# CRITICAL: Disable server-side prepared statements for pgbouncer
# Supabase pgbouncer (transaction mode) drops server-side state
# between transactions, causing DuplicatePreparedStatement errors.
# Set prepare_threshold=0 as class default for ALL psycopg connections.
# ============================================================
psycopg.Connection.prepare_threshold = 0


engine = create_async_engine(
    settings.async_database_url,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10,
)


async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def create_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"CREATE_TABLES ERROR: {e}")
    # Run migrations using direct psycopg connection (bypasses SQLAlchemy async)
    _run_migrations_sync()


def _run_migrations_sync():
    """Add missing columns using direct psycopg connection."""
    migrations = [
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS approval_status VARCHAR(50) DEFAULT 'pending'",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS approved_by UUID",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS approved_at TIMESTAMP",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS rejection_reason TEXT",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS sales_invoice_id UUID",
        # Approve all existing users (they predate the approval system)
        "UPDATE users SET approval_status = 'approved', is_active = true WHERE approval_status IS NULL OR approval_status = 'pending'",
    ]
    try:
        conn = psycopg.connect(settings.sync_database_url)
        conn.autocommit = True
        cur = conn.cursor()
        for sql in migrations:
            try:
                cur.execute(sql)
                print(f"MIGRATION OK: {sql[:60]}...")
            except Exception as e:
                print(f"MIGRATION WARN: {sql[:60]}... -> {e}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"MIGRATION CONNECT ERROR: {e}")
