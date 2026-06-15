from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings


engine = create_async_engine(settings.DATABASE_URL, future=True, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session, session.begin():
        yield session


@asynccontextmanager
async def get_session_ctx() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session, session.begin():
        yield session
