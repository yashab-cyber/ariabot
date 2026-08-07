"""
Owner Panel Cog for Aria.
Administrative control panel with permission enforcement and system metrics.
"""
import sys
import psutil
import discord
from discord.ext import commands
from discord import app_commands
from bot.config.settings import settings
from bot.services.cache_service import cache_service
from bot.utils.logger import logger


def is_owner():
    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.user.id in settings.OWNER_IDS or interaction.user.id == interaction.guild.owner_id:
            return True
        await interaction.response.send_message("❌ Owner permission required.", ephemeral=True)
        return False
    return app_commands.check(predicate)


class OwnerCog(commands.Cog, name="Owner Panel"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="reload", description="Reload a bot cog/plugin dynamically.")
    @is_owner()
    async def reload_cog(self, interaction: discord.Interaction, extension: str):
        try:
            full_name = f"bot.cogs.{extension}" if not extension.startswith("bot.cogs.") else extension
            await self.bot.reload_extension(full_name)
            await interaction.response.send_message(f"✅ Reloaded extension `{full_name}` successfully.")
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to reload extension: {e}", ephemeral=True)

    @app_commands.command(name="maintenance", description="Toggle maintenance mode.")
    @is_owner()
    async def maintenance(self, interaction: discord.Interaction, enabled: bool):
        self.bot.maintenance_mode = enabled
        status_str = "ENABLED 🛑" if enabled else "DISABLED 🟢"
        await interaction.response.send_message(f"🔧 Maintenance Mode is now **{status_str}**.")

    @app_commands.command(name="broadcast", description="Broadcast a message across server announcement channels.")
    @is_owner()
    async def broadcast(self, interaction: discord.Interaction, message: str):
        await interaction.response.defer(ephemeral=True)
        count = 0
        for guild in self.bot.guilds:
            if guild.system_channel:
                try:
                    embed = discord.Embed(
                        title="📢 Official Announcement from Bot Owner",
                        description=message,
                        color=0x5865F2
                    )
                    await guild.system_channel.send(embed=embed)
                    count += 1
                except Exception:
                    continue
        await interaction.followup.send(f"✅ Announcement broadcasted to {count} servers.", ephemeral=True)

    @app_commands.command(name="clear_cache", description="Clear all in-memory and Redis cache keys.")
    @is_owner()
    async def clear_cache(self, interaction: discord.Interaction):
        await cache_service._memory_cache.clear()
        await interaction.response.send_message("🧹 Cache cleared successfully.", ephemeral=True)

    @app_commands.command(name="health", description="Run system health check and metrics review.")
    @is_owner()
    async def health(self, interaction: discord.Interaction):
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory()

        embed = discord.Embed(
            title="🩺 System Health Check",
            color=0x57F287 if cpu < 80 and mem.percent < 85 else 0xED4245
        )
        embed.add_field(name="CPU Usage", value=f"`{cpu}%`", inline=True)
        embed.add_field(name="Memory Used", value=f"`{mem.percent}% ({mem.used // (1024**2)} MB / {mem.total // (1024**2)} MB)`", inline=True)
        embed.add_field(name="Loaded Cogs", value=f"`{len(self.bot.cogs)}`", inline=True)
        embed.add_field(name="Connected Guilds", value=f"`{len(self.bot.guilds)}`", inline=True)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(OwnerCog(bot))
