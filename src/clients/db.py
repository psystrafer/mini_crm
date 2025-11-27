from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.settings import settings

async_engine = create_async_engine(
    settings.db_dsn,
    pool_pre_ping=True,
    echo=True,
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    expire_on_commit=False,
)

async def get_session():
    try:
        yield AsyncSessionLocal
    finally:
        await async_engine.dispose()


AsyncSession = Annotated[async_sessionmaker, Depends(get_session)]
