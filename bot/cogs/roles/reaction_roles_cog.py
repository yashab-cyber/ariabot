"""
Reaction Roles Cog for Aria.
Allows server admins to create interactive button & dropdown role selectors.
"""
import discord
from discord.ext import commands
from discord import app_commands
from bot.views.reaction_roles_views import ReactionRolesView


class ReactionRolesCog(commands.Cog, name="Reaction Roles"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup_reaction_roles", description="Deploy a reaction role selector in this channel.")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_reaction_roles(
        self,
        interaction: discord.Interaction,
        title: str,
        role_1: discord.Role,
        role_2: discord.Role = None,
        role_3: discord.Role = None,
        role_4: discord.Role = None,
        role_5: discord.Role = None
    ):
        roles = [r for r in [role_1, role_2, role_3, role_4, role_5] if r]

        embed = discord.Embed(
            title=f"🎭 {title}",
            description="Select a role from the dropdown menu below to toggle it on or off!",
            color=0x5865F2
        )
        embed.set_footer(text="Reaction Roles • OpenDroid Community")

        view = ReactionRolesView(roles)
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message("✅ Reaction roles menu deployed successfully!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(ReactionRolesCog(bot))
