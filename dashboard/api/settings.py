"""
Dashboard Guild Settings REST API.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from bot.database.connection import AsyncSessionLocal
from bot.database.repositories.guild_repo import GuildRepository

router = APIRouter(prefix="/api/settings", tags=["Settings"])


class GuildSettingsUpdate(BaseModel):
    prefix: Optional[str] = None
    ai_enabled: Optional[bool] = None
    moderation_enabled: Optional[bool] = None
    welcome_enabled: Optional[bool] = None
    tickets_enabled: Optional[bool] = None
    leveling_enabled: Optional[bool] = None
    ai_provider: Optional[str] = None
    ai_model: Optional[str] = None


@router.get("/{guild_id}")
async def get_guild_settings(guild_id: int):
    async with AsyncSessionLocal() as session:
        repo = GuildRepository(session)
        config = await repo.get_or_create(guild_id)
        return {
            "guild_id": config.guild_id,
            "prefix": config.prefix,
            "ai_enabled": config.ai_enabled,
            "moderation_enabled": config.moderation_enabled,
            "welcome_enabled": config.welcome_enabled,
            "tickets_enabled": config.tickets_enabled,
            "leveling_enabled": config.leveling_enabled,
            "ai_provider": config.ai_provider,
            "ai_model": config.ai_model,
        }


@router.post("/{guild_id}")
async def update_guild_settings(guild_id: int, payload: GuildSettingsUpdate):
    async with AsyncSessionLocal() as session:
        repo = GuildRepository(session)
        data = payload.model_dump(exclude_unset=True)
        config = await repo.update_settings(guild_id, **data)
        return {"status": "success", "settings": data}
