from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import DBManager
from app.db.session import async_session
from app.models import Statistics


async def get_session() -> AsyncSession:
    async with async_session() as session:
        async with session.begin():
            yield session


async def get_statistics_manager(
    session: AsyncSession = Depends(get_session),
) -> DBManager:
    yield DBManager(session, Statistics)
