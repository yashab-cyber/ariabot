import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from bot.database.connection import Base
from bot.database.repositories.economy_repo import EconomyRepository


@pytest.fixture
async def async_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_maker() as session:
        yield session

    await engine.dispose()


@pytest.mark.asyncio
async def test_economy_daily_and_transfer(async_session):
    repo = EconomyRepository(async_session)
    user1 = await repo.get_or_create(100, 1)
    user2 = await repo.get_or_create(100, 2)

    assert user1.wallet == 100
    assert user2.wallet == 100

    # Simulate daily claim
    success, amount, msg = await repo.claim_daily(100, 1)
    assert success is True
    assert user1.wallet == 100 + amount
