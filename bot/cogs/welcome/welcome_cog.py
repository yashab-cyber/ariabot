"""
Welcome & Goodbye Cog for Aria.
Handles automated member onboarding, animated welcome embeds, goodbye messages, and auto-roles.
"""
import discord
from discord.ext import commands
from discord import app_commands
from bot.database.connection import AsyncSessionLocal
from bot.database.repositories.guild_repo import GuildRepository
from bot.utils.logger import logger


class WelcomeCog(commands.Cog, name="Welcome & Onboarding"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        async with AsyncSessionLocal() as session:
            repo = GuildRepository(session)
            config = await repo.get(member.guild.id)
            if not config or not config.welcome_enabled:
                return

            # Assign Auto Roles
            if config.auto_role_ids:
                roles_to_add = [member.guild.get_role(rid) for rid in config.auto_role_ids if member.guild.get_role(rid)]
                if roles_to_add:
                    try:
                        await member.add_roles(*roles_to_add, reason="Auto Role Assignment")
                    except Exception as e:
                        logger.error(f"Failed auto roles assignment for {member.name}: {e}")

            # Send Welcome Channel Message
            if config.welcome_channel_id:
                channel = member.guild.get_channel(config.welcome_channel_id)
                if channel:
                    msg = config.welcome_message.format(
                        user=member.mention,
                        server=member.guild.name,
                        count=member.guild.member_count
                    )
                    embed = discord.Embed(
                        title=f"👋 Welcome to {member.guild.name}!",
                        description=msg,
                        color=0x57F287
                    )
                    embed.set_thumbnail(url=member.display_avatar.url)
                    embed.set_footer(text=f"Member #{member.guild.member_count} • OpenDroid Community")
                    await channel.send(embed=embed)

            # Auto DM Welcome
            if config.auto_dm_welcome:
                try:
                    dm_embed = discord.Embed(
                        title=f"Welcome to {member.guild.name}!",
                        description=f"Hey {member.name}! Thanks for joining our server. Be sure to check the rules and enjoy your stay!",
                        color=0x5865F2
                    )
                    await member.send(embed=dm_embed)
                except Exception:
                    pass

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        async with AsyncSessionLocal() as session:
            repo = GuildRepository(session)
            config = await repo.get(member.guild.id)
            if not config or not config.goodbye_channel_id:
                return

            channel = member.guild.get_channel(config.goodbye_channel_id)
            if channel:
                embed = discord.Embed(
                    description=f"👋 **{member.display_name}** has left the server.",
                    color=0x95A5A6
                )
                await channel.send(embed=embed)

    @app_commands.command(name="setup_welcome", description="Configure server welcome channel and message.")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_welcome(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        message: str = "Welcome {user} to {server}!"
    ):
        async with AsyncSessionLocal() as session:
            repo = GuildRepository(session)
            await repo.update_settings(
                interaction.guild_id,
                welcome_enabled=True,
                welcome_channel_id=channel.id,
                welcome_message=message
            )

        embed = discord.Embed(
            title="✅ Welcome System Configured",
            description=f"**Channel:** {channel.mention}\n**Message Template:**\n`{message}`",
            color=0x57F287
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))
