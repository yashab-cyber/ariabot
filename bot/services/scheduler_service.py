"""
Scheduler Service for executing recurring background jobs.
Handles reminders, daily announcements, auto cleanup, and metrics updates.
"""
import asyncio
from datetime import datetime
from bot.database.connection import AsyncSessionLocal
from bot.database.repositories.reminder_repo import ReminderRepository
from bot.utils.logger import logger


class SchedulerService:
    def __init__(self, bot=None):
        self.bot = bot
        self._task: asyncio.Task = None
        self._running = False

    def start(self, bot) -> None:
        self.bot = bot
        self._running = True
        self._task = asyncio.create_task(self._loop())
        logger.info("Scheduler Service started successfully.")

    def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
        logger.info("Scheduler Service stopped.")

    async def _loop(self) -> None:
        while self._running:
            try:
                await self._check_due_reminders()
                await asyncio.sleep(15)  # Poll every 15 seconds
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Scheduler loop error: {e}")
                await asyncio.sleep(15)

    async def _check_due_reminders(self) -> None:
        if not self.bot:
            return

        async with AsyncSessionLocal() as session:
            repo = ReminderRepository(session)
            due_reminders = await repo.get_due_reminders()

            for rem in due_reminders:
                try:
                    user = self.bot.get_user(rem.user_id) or await self.bot.fetch_user(rem.user_id)
                    if user:
                        embed = {
                            "title": "⏰ Reminder!",
                            "description": rem.message,
                            "color": 0x5865F2,
                            "timestamp": rem.created_at.isoformat()
                        }
                        await user.send(content=f"Hello {user.mention}, here is your reminder!", embed=self._dict_to_embed(embed))

                    await repo.delete(rem)
                except Exception as e:
                    logger.error(f"Failed to deliver reminder #{rem.id}: {e}")
                    await repo.delete(rem)


    def _dict_to_embed(self, d: dict):
        import discord
        embed = discord.Embed(
            title=d.get("title"),
            description=d.get("description"),
            color=d.get("color", 0x5865F2)
        )
        return embed


scheduler_service = SchedulerService()
