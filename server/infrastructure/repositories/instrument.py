from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from infrastructure.repositories.base import BaseRepository
from domain.instrument_model import Instrument

from typing import Optional


class InstrumentRepository(BaseRepository[Instrument]):
    def __init__(self, session: AsyncSession):
        super().__init__(Instrument, session)
    
    async def get_by_code(self, code: str) -> Optional[Instrument]:
        query = select(self.model).where(self.model.code == code)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()