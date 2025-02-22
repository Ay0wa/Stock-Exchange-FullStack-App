import pytest
from infrastructure.repositories.instrument import InstrumentRepository

@pytest.mark.asyncio
async def test_get_instrument_by_code(db_session, sample_instrument):
    repo = InstrumentRepository(db_session)
    
    instrument = await repo.get_by_code("AAPL")
    
    assert instrument is not None
    assert instrument.code == "AAPL"
    assert instrument.name == "Apple Inc."
    
@pytest.mark.asyncio
async def test_get_nonexistent_instrument_by_code(db_session):
    repo = InstrumentRepository(db_session)
    
    instrument = await repo.get_by_code("NONEXISTENT")
    
    assert instrument is None