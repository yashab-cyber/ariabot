"""
Tickets Cog for Aria.
Configures and launches ticket support system.
"""
import discord
from discord.ext import commands
from discord import app_commands
from bot.views.ticket_views import TicketLaunchView
from bot.database.connection import AsyncSessionLocal
from bot.database.repositories.guild_repo import GuildRepository


class TicketsCog(commands.Cog, name="Tickets"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup_tickets", description="Deploy support ticket creation panel.")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_tickets(self, interaction: discord.Interaction, category: discord.CategoryChannel):
        async with AsyncSessionLocal() as session:
            repo = GuildRepository(session)
            await repo.update_settings(
                interaction.guild_id,
                tickets_enabled=True,
                ticket_category_id=category.id
            )

        embed = discord.Embed(
            title="📩 OpenDroid Support Desk",
            description="Need help or have a question? Select a ticket category from the dropdown menu below to open a private ticket with our staff.",
            color=0x5865F2
        )
        embed.set_footer(text="Support Ticket System • OpenDroid Community")

        await interaction.channel.send(embed=embed, view=TicketLaunchView())
        await interaction.response.send_message(f"✅ Ticket panel deployed under category: {category.name}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(TicketsCog(bot))
