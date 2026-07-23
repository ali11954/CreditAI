import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.database import engine, Base
from app.models import *  # noqa: ensure all models are imported


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")


if __name__ == "__main__":
    asyncio.run(init_db())
