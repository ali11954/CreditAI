from typing import AsyncGenerator

from sqlalchemy import event
from sqlalchemy.dialects.postgresql.psycopg import PGDialect_psycopg
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

# ============================================================
# CRITICAL: Disable server-side prepared statements
# Supabase pgbouncer (transaction mode) drops server-side state
# between transactions, causing DuplicatePreparedStatement errors.
# We patch the dialect's connect() to force prepare_threshold=0.
# ============================================================
_original_dialect_connect = PGDialect_psycopg.connect


def _patched_connect(self, *cargs, **cparams):
    cparams = dict(cparams)
    cparams["prepare_threshold"] = 0
    return _original_dialect_connect(self, *cargs, **cparams)


PGDialect_psycopg.connect = _patched_connect  # type: ignore


engine = create_async_engine(
    settings.async_database_url,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10,
)


@event.listens_for(engine.pool, "checkout")
def _on_checkout(conn, rec, proxy):
    if hasattr(conn, "prepare_threshold"):
        conn.prepare_threshold = 0


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
