"""
Guild Repository for managing Guild Configuration.
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from bot.database.models.guild import GuildConfig
from bot.database.repositories.base import BaseRepository


class GuildRepository(BaseRepository[GuildConfig]):
    def __init__(self, session: AsyncSession):
        super().__init__(GuildConfig, session)

    async def get_or_create(self, guild_id: int) -> GuildConfig:
        guild_config = await self.get(guild_id)
        if not guild_config:
            guild_config = await self.create(guild_id=guild_id)
        return guild_config

    async def update_settings(self, guild_id: int, **kwargs) -> GuildConfig:
        config = await self.get_or_create(guild_id)
        return await self.update(config, **kwargs)
