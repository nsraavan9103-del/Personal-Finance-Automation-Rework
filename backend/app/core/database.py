from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Use NullPool for testing to avoid connection pool issues
engine = create_async_engine(
    settings.DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://'),
    echo=settings.DEBUG,
    poolclass=NullPool
)

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
