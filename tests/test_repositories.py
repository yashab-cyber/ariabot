import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from bot.database.connection import Base
from bot.database.repositories.guild_repo import GuildRepository
from bot.database.repositories.mod_repo import ModerationRepository


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
async def test_guild_repository_get_or_create(async_session):
    repo = GuildRepository(async_session)
    config = await repo.get_or_create(123456789)
    assert config.guild_id == 123456789
    assert config.prefix == "!"

    # Update setting
    updated = await repo.update_settings(123456789, prefix="?")
    assert updated.prefix == "?"


@pytest.mark.asyncio
async def test_moderation_repository_case_creation(async_session):
    repo = ModerationRepository(async_session)
    case1 = await repo.create_case(123, 456, 789, "WARN", "Spamming")
    assert case1.case_number == 1
    assert case1.action == "WARN"

    case2 = await repo.create_case(123, 456, 789, "BAN", "Severe rule violation")
    assert case2.case_number == 2
    assert case2.action == "BAN"
