from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base


class DBManager:
    def __init__(self, session: AsyncSession, model: Base):
        self.session = session
        self.model = model

    async def create(self, obj_in: dict):
        obj_in = self.model(**obj_in)
        self.session.add(obj_in)
        await self.session.flush()
        await self.session.refresh(obj_in)
        return obj_in

    async def clear(self):
        await self.session.execute(delete(self.model))

    async def list(self, *aggregators, order_by: str = None):
        query = select(self.model)
        for aggregator in aggregators:
            query = aggregator(query)
        if order_by:
            try:
                order_by_field = getattr(self.model, order_by)
                if order_by.startswith("-"):
                    order_by_field = order_by_field.desc()
                query = query.order_by(order_by_field)
            except AttributeError:
                pass
        return (await self.session.execute(query)).scalars().all()
