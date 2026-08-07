"""
Leveling Repository for handling user XP and rank data.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from bot.database.models.leveling import LevelUser
from bot.database.repositories.base import BaseRepository


class LevelingRepository(BaseRepository[LevelUser]):
    def __init__(self, session: AsyncSession):
        super().__init__(LevelUser, session)

    async def get_or_create_user(self, guild_id: int, user_id: int) -> LevelUser:
        stmt = select(LevelUser).where(
            LevelUser.guild_id == guild_id,
            LevelUser.user_id == user_id
        )
        res = await self.session.execute(stmt)
        user = res.scalar_one_or_none()
        if not user:
            user = LevelUser(guild_id=guild_id, user_id=user_id, xp=0, level=0)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
        return user

    async def add_xp(self, guild_id: int, user_id: int, xp_amount: int) -> tuple[LevelUser, bool]:
        user = await self.get_or_create_user(guild_id, user_id)
        user.xp += xp_amount
        user.last_xp_given = datetime.utcnow()

        # Simple formula for level calculation: XP = 100 * level^1.5
        new_level = int((user.xp / 100) ** (1 / 1.5))
        leveled_up = new_level > user.level
        if leveled_up:
            user.level = new_level

        await self.session.commit()
        await self.session.refresh(user)
        return user, leveled_up

    async def get_leaderboard(self, guild_id: int, limit: int = 10) -> List[LevelUser]:
        stmt = select(LevelUser).where(
            LevelUser.guild_id == guild_id
        ).order_by(LevelUser.xp.desc()).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
