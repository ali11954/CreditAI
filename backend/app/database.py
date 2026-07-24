from typing import AsyncGenerator

import psycopg as _psycopg
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

# Monkey-patch psycopg to always disable prepared statements
# This is necessary because Supabase pgbouncer (transaction mode)
# does not support server-side prepared statements
_original_connect = _psycopg.Connection.connect.__func__


@classmethod  # type: ignore
def _safe_connect(cls, *args, **kwargs):
    kwargs.setdefault("prepare_threshold", 0)
    return _original_connect(cls, *args, **kwargs)


_psycopg.Connection.connect = _safe_connect  # type: ignore


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
