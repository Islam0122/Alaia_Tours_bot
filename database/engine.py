import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .model import Base

DB_LITE="sqlite+aiosqlite:///db.sqlite3"

engine = create_async_engine(DB_LITE, echo=True) # --> sqlite3
# engine = create_async_engine(os.getenv('DB_URL'), echo=True)
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
