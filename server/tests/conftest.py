import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from typing import AsyncGenerator

from domain.enums import OrderSide, OrderStatus
from domain.base import Base
from domain.order_model import Order
from domain.instrument_model import Instrument
from domain.user_model import User

DATABASE_URL = "postgresql+asyncpg://postgres:1111@localhost:5432/test_trading_db"

@pytest.fixture
async def engine():
    engine = create_async_engine(DATABASE_URL, echo=False)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        yield engine
    finally:
        await engine.dispose()
        await asyncio.sleep(0.1)

@pytest.fixture()
async def db_session(engine) -> AsyncGenerator:
    session_maker = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()

@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    user = User(
        username="testuser",
        email="test@gmail.com",
        hashed_password="test_password",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture
async def sample_instrument(db_session: AsyncSession) -> Instrument:
    instrument = Instrument(
        code="AAPL",
        name="Apple Inc.",
        min_volume=1,
        max_volume=3,
        tick_size=1.0,
    )
    
    db_session.add(instrument)
    await db_session.commit()
    await db_session.refresh(instrument)
    return instrument

@pytest.fixture
async def sample_active_order(db_session: AsyncSession, sample_instrument: Instrument, test_user: User) -> Order:
    order = Order(
        instrument_id=sample_instrument.id,
        side=OrderSide.BUY,
        price=150.0,
        volume=100,
        status=OrderStatus.ACTIVE,
        user_id=test_user.id,
    )
    db_session.add(order)
    await db_session.commit()
    await db_session.refresh(order)
    return order

@pytest.fixture
async def sample_filled_order(db_session: AsyncSession, sample_instrument: Instrument, test_user: User) -> Order:
    order = Order(
        instrument_id=sample_instrument.id,
        side=OrderSide.SELL,
        price=160.0,
        volume=50,
        status=OrderStatus.FILLED,
        user_id=test_user.id,
    )
    db_session.add(order)
    await db_session.commit()
    await db_session.refresh(order)
    return order

@pytest.fixture(autouse=True)
async def clean_database(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)