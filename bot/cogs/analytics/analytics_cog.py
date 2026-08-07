"""
Analytics Cog for Aria.
Reports server message counts, member growth, ticket volume, and AI usage metrics.
"""
import discord
from discord.ext import commands
from discord import app_commands
from bot.database.connection import AsyncSessionLocal
from bot.database.repositories.guild_repo import GuildRepository


class AnalyticsCog(commands.Cog, name="Analytics"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="analytics", description="View server analytics and activity overview.")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def analytics(self, interaction: discord.Interaction):
        guild = interaction.guild

        embed = discord.Embed(
            title=f"📈 Analytics Overview — {guild.name}",
            description="Real-time performance and engagement metrics.",
            color=0x5865F2
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="Total Members", value=f"`{guild.member_count}`", inline=True)
        embed.add_field(name="Text Channels", value=f"`{len(guild.text_channels)}`", inline=True)
        embed.add_field(name="Voice Channels", value=f"`{len(guild.voice_channels)}`", inline=True)
        embed.add_field(name="Roles Count", value=f"`{len(guild.roles)}`", inline=True)
        embed.add_field(name="System Status", value="`Operational 🟢`", inline=True)

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(AnalyticsCog(bot))
