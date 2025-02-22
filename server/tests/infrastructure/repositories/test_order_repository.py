import pytest

from infrastructure.repositories.order import OrderRepository
from infrastructure.repositories.instrument import InstrumentRepository

from domain.order_model import Order, OrderStatus

@pytest.mark.asyncio
async def test_get_active_orders(db_session, sample_active_order, sample_filled_order):
    repo = OrderRepository(db_session)
    
    active_orders = await repo.get_active_orders()
    
    assert len(active_orders) == 1
    assert active_orders[0].id == sample_active_order.id
    assert active_orders[0].status == OrderStatus.ACTIVE
    
@pytest.mark.asyncio
async def test_get_active_orders_by_instrument(
    db_session,
    sample_active_order,
    sample_instrument,
):
    repo = OrderRepository(db_session)
    
    active_orders = await repo.get_active_orders(instrument_id=sample_instrument.id)
    
    assert len(active_orders) == 1
    assert active_orders[0].instrument_id == sample_instrument.id
    
@pytest.mark.asyncio
async def test_get_active_orders_empty(db_session, sample_filled_order):
    repo = OrderRepository(db_session)
    
    active_orders = await repo.get_active_orders()
    
    assert len(active_orders) == 0