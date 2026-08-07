"""
Verification Cog for Aria.
Configures and launches verification panels.
"""
import discord
from discord.ext import commands
from discord import app_commands
from bot.views.verification_views import VerificationLaunchView
from bot.database.connection import AsyncSessionLocal
from bot.database.repositories.guild_repo import GuildRepository


class VerificationCog(commands.Cog, name="Verification"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup_verification", description="Deploy the verification panel in this channel.")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_verification(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
        verification_type: str = "captcha"
    ):
        async with AsyncSessionLocal() as session:
            repo = GuildRepository(session)
            await repo.update_settings(
                interaction.guild_id,
                verification_enabled=True,
                verified_role_id=role.id,
                verification_type=verification_type
            )

        embed = discord.Embed(
            title="🛡️ Server Security Verification",
            description=f"To gain full access to **{interaction.guild.name}**, please click the button below to complete security verification.",
            color=0x5865F2
        )
        embed.set_footer(text="OpenDroid Security Verification")

        await interaction.channel.send(embed=embed, view=VerificationLaunchView())
        await interaction.response.send_message(f"✅ Verification panel deployed! Assigning role: {role.mention}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(VerificationCog(bot))
