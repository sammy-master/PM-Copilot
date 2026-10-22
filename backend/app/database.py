"""
PM Copilot - Database Connection
----------------------------------
Sets up the async SQLAlchemy engine and session for PostgreSQL.
Uses async sessions so FastAPI can handle many requests concurrently.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


# Create the async engine (the connection to PostgreSQL)
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,   # Log SQL queries in debug mode
    future=True,
)

# Session factory — creates a new DB session per request
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Base class for all ORM models
class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    """
    FastAPI dependency — provides a DB session to each API route.
    The session is automatically closed when the request is done.

    Usage in a route:
        async def my_route(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        yield session


async def create_tables() -> None:
    """
    Creates all database tables on app startup.
    Called from main.py lifespan event.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
