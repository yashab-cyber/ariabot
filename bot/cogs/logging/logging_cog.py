"""
Audit Logging Cog for Aria.
Listens to server events (message edit/delete, member updates, voice activity) and logs to configured audit channel.
"""
import discord
from discord.ext import commands
from bot.database.connection import AsyncSessionLocal
from bot.database.repositories.guild_repo import GuildRepository
from bot.utils.logger import logger


class LoggingCog(commands.Cog, name="Audit Logging"):
    def __init__(self, bot):
        self.bot = bot

    async def _get_audit_channel(self, guild_id: int) -> discord.TextChannel | None:
        async with AsyncSessionLocal() as session:
            repo = GuildRepository(session)
            config = await repo.get(guild_id)
            if config and config.logging_enabled and config.audit_log_channel_id:
                guild = self.bot.get_guild(guild_id)
                if guild:
                    return guild.get_channel(config.audit_log_channel_id)
        return None

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        channel = await self._get_audit_channel(message.guild.id)
        if channel:
            embed = discord.Embed(
                title="🗑️ Message Deleted",
                description=f"**Author:** {message.author.mention} (`{message.author.id}`)\n**Channel:** {message.channel.mention}\n**Content:**\n{message.content or '*[No Text / Attachment]*'}",
                color=0xED4245
            )
            embed.set_footer(text=f"Message ID: {message.id}")
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.author.bot or not before.guild or before.content == after.content:
            return

        channel = await self._get_audit_channel(before.guild.id)
        if channel:
            embed = discord.Embed(
                title="✏️ Message Edited",
                description=f"**Author:** {before.author.mention}\n**Channel:** {before.channel.mention}\n**Before:** {before.content}\n**After:** {after.content}",
                color=0xFEE75C
            )
            await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(LoggingCog(bot))
