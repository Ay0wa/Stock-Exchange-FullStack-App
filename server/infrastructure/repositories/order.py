from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from typing import Optional, List

from infrastructure.repositories.base import BaseRepository
from domain.order_model import Order, OrderStatus


class OrderRepository(BaseRepository[Order]):
    def __init__(self, session: AsyncSession):
        super().__init__(Order, session)
        
    async def get_active_orders(self, instrument_id: Optional[int] = None) -> List[Order]:
        query = select(self.model).where(self.model.status == OrderStatus.ACTIVE)
        if instrument_id is not None:
            query = query.where(self.model.instrument_id == instrument_id)
        result = await self.session.execute(query)
        return result.scalars().all()