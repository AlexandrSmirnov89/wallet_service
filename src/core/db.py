from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.core.config import settings

# 🔹 Асинхронный движок для FastAPI
async_engine = create_async_engine(settings.DATABASE_URL, echo=False, pool_size=50, max_overflow=100)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

# 🔹 Синхронный движок для Celery
sync_engine = create_engine(settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql"),
                            echo=False,
                            pool_size=50,
                            max_overflow=100,
                            pool_timeout=60)

SyncSessionLocal = sessionmaker(bind=sync_engine, expire_on_commit=False, class_=Session)

# Асинхронная сессия для FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Синхронная сессия для Celery
def get_sync_db():
    with SyncSessionLocal() as session:
        return session
