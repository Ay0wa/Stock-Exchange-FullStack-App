import pytest

from infrastructure.repositories.base import BaseRepository
from domain.instrument_model import Instrument

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.repositories.base import BaseRepository
from domain.instrument_model import Instrument

@pytest.mark.asyncio
async def test_base_repository_create(db_session: AsyncSession):
    repo = BaseRepository(Instrument, db_session)
    new_instrument = Instrument(
        code="GOOGL",
        name="Google LLC",
        min_volume=1,
        max_volume=3,
        tick_size=1.0,
    )
    
    try:
        created = await repo.create(new_instrument)
        await db_session.commit()
        
        assert created.id is not None
        assert created.code == "GOOGL"
        assert created.min_volume == 1
        assert created.max_volume == 3
        assert created.tick_size == 1.0

        saved = await repo.get(created.id)
        assert saved is not None
        assert saved.code == "GOOGL"
        
    finally:
        await db_session.rollback()
        
@pytest.mark.asyncio
async def test_base_repository_get(db_session, sample_instrument):
    repo = BaseRepository(Instrument, db_session)
    
    instrument = await repo.get(sample_instrument.id)
    
    assert instrument is not None
    assert instrument.id == sample_instrument.id
    
@pytest.mark.asyncio
async def test_base_repository_list(db_session, sample_instrument):
    repo = BaseRepository(Instrument, db_session)
    
    instruments = await repo.list()
    
    assert len(instruments) >= 1
    assert any(i.id == sample_instrument.id for i in instruments)
    
@pytest.mark.asyncio
async def test_base_repository_update(db_session, sample_instrument):
    repo = BaseRepository(Instrument, db_session)
    
    sample_instrument.name = "Updated Name"
    updated = await repo.update(sample_instrument)
    await db_session.refresh(updated)
    
    assert updated.name == "Updated Name"
    
    fresh = await repo.get(sample_instrument.id)
    assert fresh.name == "Updated Name"