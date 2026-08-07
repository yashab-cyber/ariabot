"""
Economy Repository for wallet, bank, daily streaks, inventory.
"""
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from bot.database.models.economy import EconomyUser
from bot.database.repositories.base import BaseRepository


class EconomyRepository(BaseRepository[EconomyUser]):
    def __init__(self, session: AsyncSession):
        super().__init__(EconomyUser, session)

    async def get_or_create(self, guild_id: int, user_id: int) -> EconomyUser:
        stmt = select(EconomyUser).where(
            EconomyUser.guild_id == guild_id,
            EconomyUser.user_id == user_id
        )
        res = await self.session.execute(stmt)
        user = res.scalar_one_or_none()
        if not user:
            user = EconomyUser(guild_id=guild_id, user_id=user_id, wallet=100, bank=0)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
        return user

    async def claim_daily(self, guild_id: int, user_id: int) -> tuple[bool, int, str]:
        user = await self.get_or_create(guild_id, user_id)
        now = datetime.utcnow()
        if user.last_daily:
            delta = now - user.last_daily
            if delta < timedelta(hours=20):
                remaining = timedelta(hours=20) - delta
                hours, remainder = divmod(remaining.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                return False, 0, f"You must wait {hours}h {minutes}m before claiming daily reward."
            
            if delta > timedelta(hours=48):
                user.daily_streak = 1
            else:
                user.daily_streak += 1
        else:
            user.daily_streak = 1

        reward = 200 + (user.daily_streak * 20)
        user.wallet += reward
        user.last_daily = now
        await self.session.commit()
        await self.session.refresh(user)
        return True, reward, f"Claimed {reward} coins! Daily Streak: {user.daily_streak} days."

    async def get_leaderboard(self, guild_id: int, limit: int = 10) -> List[EconomyUser]:
        stmt = select(EconomyUser).where(
            EconomyUser.guild_id == guild_id
        ).order_by((EconomyUser.wallet + EconomyUser.bank).desc()).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
