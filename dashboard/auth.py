"""
Discord OAuth2 Authentication Module for Dashboard.
"""
from typing import Optional
import aiohttp
from fastapi import Request, HTTPException, status
from bot.config.settings import settings

DISCORD_API_BASE = "https://discord.com/api/v10"


async def get_discord_user(access_token: str) -> dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{DISCORD_API_BASE}/users/@me", headers=headers) as resp:
            if resp.status == 200:
                return await resp.json()
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Discord token.")


async def get_user_guilds(access_token: str) -> list:
    headers = {"Authorization": f"Bearer {access_token}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{DISCORD_API_BASE}/users/@me/guilds", headers=headers) as resp:
            if resp.status == 200:
                return await resp.json()
            return []
