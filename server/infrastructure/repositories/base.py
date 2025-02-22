from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from typing import Generic, TypeVar, Type, Optional, List

from domain.base import Base


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session
    
    async def get(self, id: str) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def list(self) -> List[ModelType]:
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def create(self, instance: ModelType):
        self.session.add(instance)
        await self.session.flush()
        return instance
    
    async def update(self, instance: ModelType) -> ModelType:
        await self.session.merge(instance)
        await self.session.flush()
        return instance