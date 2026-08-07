"""
Reminders Cog for Aria.
Schedules one-time or recurring reminders.
"""
from datetime import datetime, timedelta
import discord
from discord.ext import commands
from discord import app_commands
from bot.database.connection import AsyncSessionLocal
from bot.database.repositories.reminder_repo import ReminderRepository


class RemindersCog(commands.Cog, name="Reminders"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="remind", description="Set a reminder for minutes in the future.")
    async def remind(self, interaction: discord.Interaction, minutes: int, message: str):
        if minutes <= 0:
            await interaction.response.send_message("Minutes must be a positive integer.", ephemeral=True)
            return

        target_time = datetime.utcnow() + timedelta(minutes=minutes)

        async with AsyncSessionLocal() as session:
            repo = ReminderRepository(session)
            rem = await repo.create(
                user_id=interaction.user.id,
                channel_id=interaction.channel_id,
                guild_id=interaction.guild_id,
                message=message,
                remind_at=target_time
            )

        embed = discord.Embed(
            title="⏰ Reminder Scheduled",
            description=f"I will remind you in **{minutes} minutes**:\n> {message}",
            color=0x5865F2
        )
        embed.set_footer(text=f"Scheduled for {target_time.strftime('%Y-%m-%d %H:%M UTC')}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="reminders", description="List your active scheduled reminders.")
    async def reminders(self, interaction: discord.Interaction):
        async with AsyncSessionLocal() as session:
            repo = ReminderRepository(session)
            user_rems = await repo.get_user_reminders(interaction.user.id)

        if not user_rems:
            await interaction.response.send_message("You have no active scheduled reminders.", ephemeral=True)
            return

        lines = [f"**#{r.id}** ({r.remind_at.strftime('%H:%M UTC')}): {r.message}" for r in user_rems]
        embed = discord.Embed(
            title="⏰ Active Reminders",
            description="\n".join(lines),
            color=0x5865F2
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(RemindersCog(bot))
