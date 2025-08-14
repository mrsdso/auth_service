from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from .config import settings

# Создание асинхронного движка для PostgreSQL
engine = create_async_engine(
    settings.database_url.replace("postgresql://", "postgresql+asyncpg://"),
    echo=True
)

# Создание базового класса для моделей
Base = declarative_base()

# Создание фабрики сессий
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Dependency для получения сессии базы данных
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
