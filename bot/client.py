"""
AriaBot Core Client Class.
Inherits from discord.ext.commands.Bot. Handles cog discovery, plugin management, and events.
"""
import sys
from typing import List, Optional
import discord
from discord.ext import commands
from bot.config.settings import settings
from bot.database.connection import init_db
from bot.services.cache_service import cache_service
from bot.services.scheduler_service import scheduler_service
from bot.utils.logger import logger


class AriaBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True
        intents.guilds = True
        intents.voice_states = True

        super().__init__(
            command_prefix=settings.BOT_PREFIX,
            intents=intents,
            help_command=None,
        )

        self.maintenance_mode: bool = False
        self.initial_cogs: List[str] = [
            "bot.cogs.ai.ai_cog",
            "bot.cogs.moderation.moderation_cog",
            "bot.cogs.welcome.welcome_cog",
            "bot.cogs.verification.verification_cog",
            "bot.cogs.tickets.tickets_cog",
            "bot.cogs.roles.reaction_roles_cog",
            "bot.cogs.polls.polls_cog",
            "bot.cogs.suggestions.suggestions_cog",
            "bot.cogs.leveling.leveling_cog",
            "bot.cogs.economy.economy_cog",
            "bot.cogs.reminders.reminders_cog",
            "bot.cogs.community.community_cog",
            "bot.cogs.utility.utility_cog",
            "bot.cogs.fun.fun_cog",
            "bot.cogs.analytics.analytics_cog",
            "bot.cogs.logging.logging_cog",
            "bot.cogs.owner.owner_cog",
        ]

    async def setup_hook(self) -> None:
        """Called automatically during bot initialization before login."""
        logger.info("Initializing database schema...")
        await init_db()

        logger.info("Initializing cache service...")
        await cache_service.initialize()

        logger.info("Loading Cogs/Plugins...")
        for cog in self.initial_cogs:
            try:
                await self.load_extension(cog)
                logger.info(f"Loaded extension: {cog}")
            except Exception as e:
                logger.error(f"Failed to load extension {cog}: {e}")

        # Start Scheduler
        scheduler_service.start(self)

        # Sync slash commands with Discord API
        if settings.DISCORD_GUILD_ID:
            guild = discord.Object(id=settings.DISCORD_GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            logger.info(f"Slash command tree synced for guild {settings.DISCORD_GUILD_ID}.")
        else:
            await self.tree.sync()
            logger.info("Slash command tree synced globally.")

    async def on_ready(self) -> None:
        logger.info(f"⚡ Aria is online and ready! Logged in as {self.user} (ID: {self.user.id})")
        logger.info(f"Connected Guilds: {len(self.guilds)} | Total Users: {sum(g.member_count for g in self.guilds)}")
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="/ask | OpenDroid AI Bot"
            )
        )

    async def on_tree_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        """Global error handler for slash commands."""
        logger.error(f"Command Error ({interaction.command.name if interaction.command else 'Unknown'}): {error}")

        embed = discord.Embed(
            title="⚠️ Command Error",
            description="An unexpected error occurred while executing this command.",
            color=0xED4245
        )
        if isinstance(error, discord.app_commands.MissingPermissions):
            embed.description = "❌ You do not have permission to execute this command."
        elif isinstance(error, discord.app_commands.CommandOnCooldown):
            embed.description = f"⏳ Command is on cooldown. Try again in {error.retry_after:.1f}s."

        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)


bot = AriaBot()
