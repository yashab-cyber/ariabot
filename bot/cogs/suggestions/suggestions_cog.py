"""
Suggestions Cog for Aria.
Community voting and staff status management for suggestions.
"""
import discord
from discord.ext import commands
from discord import app_commands
from bot.database.connection import AsyncSessionLocal
from bot.database.repositories.guild_repo import GuildRepository
from bot.database.repositories.base import BaseRepository
from bot.database.models.suggestion import Suggestion
from bot.views.suggestion_views import SuggestionView


class SuggestionsCog(commands.Cog, name="Suggestions"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup_suggestions", description="Set the channel for community suggestions.")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_suggestions(self, interaction: discord.Interaction, channel: discord.TextChannel):
        async with AsyncSessionLocal() as session:
            repo = GuildRepository(session)
            await repo.update_settings(interaction.guild_id, suggestions_enabled=True, suggestion_channel_id=channel.id)

        await interaction.response.send_message(f"✅ Suggestion channel set to {channel.mention}.", ephemeral=True)

    @app_commands.command(name="suggest", description="Submit a community suggestion.")
    async def suggest(self, interaction: discord.Interaction, idea: str):
        async with AsyncSessionLocal() as session:
            guild_repo = GuildRepository(session)
            config = await guild_repo.get_or_create(interaction.guild_id)

            if not config.suggestion_channel_id:
                await interaction.response.send_message("❌ Suggestions channel has not been set up yet.", ephemeral=True)
                return

            channel = interaction.guild.get_channel(config.suggestion_channel_id)
            if not channel:
                await interaction.response.send_message("❌ Invalid suggestions channel.", ephemeral=True)
                return

            embed = discord.Embed(
                title="💡 New Suggestion",
                description=idea,
                color=0x3498DB
            )
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
            embed.add_field(name="Status", value="📌 Pending Review", inline=True)

            msg = await channel.send(embed=embed)

            # Store in DB
            repo = BaseRepository(Suggestion, session)
            sug = await repo.create(
                guild_id=interaction.guild_id,
                author_id=interaction.user.id,
                message_id=msg.id,
                content=idea,
                status="Pending"
            )

            # Edit message with interactive view
            await msg.edit(view=SuggestionView(suggestion_id=sug.id, upvote_count=0, downvote_count=0))

        await interaction.response.send_message(f"✅ Suggestion submitted to {channel.mention}!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(SuggestionsCog(bot))
