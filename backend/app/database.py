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
# We patch psycopg.Connection.connect to force prepare_threshold=0.
# ============================================================
_original_connect = psycopg.Connection.connect


def _patched_connect(*args, **kwargs):
    conn = _original_connect(*args, **kwargs)
    conn.prepare_threshold = 0
    return conn


psycopg.Connection.connect = _patched_connect  # type: ignore


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
    except Exception:
        pass
