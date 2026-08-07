"""
Reminder Repository for fetching and processing scheduled reminders.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from bot.database.models.reminder import Reminder
from bot.database.repositories.base import BaseRepository


class ReminderRepository(BaseRepository[Reminder]):
    def __init__(self, session: AsyncSession):
        super().__init__(Reminder, session)

    async def get_due_reminders(self) -> List[Reminder]:
        now = datetime.utcnow()
        stmt = select(Reminder).where(Reminder.remind_at <= now)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_user_reminders(self, user_id: int) -> List[Reminder]:
        stmt = select(Reminder).where(Reminder.user_id == user_id).order_by(Reminder.remind_at.asc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
