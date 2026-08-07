"""
Moderation Cog for Aria.
Includes AutoMod, warning system, timeouts, bans, kicks, cases, notes, and appeals.
"""
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from datetime import timedelta
import re
from bot.database.connection import AsyncSessionLocal
from bot.database.repositories.mod_repo import ModerationRepository
from bot.database.repositories.guild_repo import GuildRepository
from bot.utils.logger import logger


class ModerationCog(commands.Cog, name="Moderation"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        async with AsyncSessionLocal() as session:
            guild_repo = GuildRepository(session)
            config = await guild_repo.get_or_create(message.guild.id)
            if not config.moderation_enabled:
                return

            # Check invite link AutoMod
            if config.automod_invite_links:
                if re.search(r"(discord\.gg|discord\.com/invite)/[a-zA-Z0-9]+", message.content):
                    await message.delete()
                    await message.channel.send(f"⚠️ {message.author.mention}, invite links are not allowed in this server.", delete_after=5)
                    return

            # Check mass mentions
            if config.automod_mass_mentions > 0 and len(message.mentions) > config.automod_mass_mentions:
                await message.delete()
                await message.channel.send(f"⚠️ {message.author.mention}, mass mentions are not allowed.", delete_after=5)
                return

            # Check bad words
            if config.automod_bad_words and config.bad_words_list:
                for bad_word in config.bad_words_list:
                    if bad_word.lower() in message.content.lower():
                        await message.delete()
                        await message.channel.send(f"⚠️ {message.author.mention}, your message contained blocked language.", delete_after=5)
                        return

    @app_commands.command(name="warn", description="Issue a formal warning to a user.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        async with AsyncSessionLocal() as session:
            repo = ModerationRepository(session)
            await repo.add_warning(interaction.guild_id, user.id, interaction.user.id, reason)
            case = await repo.create_case(interaction.guild_id, user.id, interaction.user.id, "WARN", reason)

        embed = discord.Embed(
            title=f"⚠️ Warning Issued (Case #{case.case_number})",
            description=f"**User:** {user.mention}\n**Reason:** {reason}\n**Moderator:** {interaction.user.mention}",
            color=0xFEE75C
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="warnings", description="View warnings for a user.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warnings(self, interaction: discord.Interaction, user: discord.Member):
        async with AsyncSessionLocal() as session:
            repo = ModerationRepository(session)
            warns = await repo.get_user_warnings(interaction.guild_id, user.id)

        if not warns:
            await interaction.response.send_message(f"No warning records found for {user.mention}.", ephemeral=True)
            return

        desc = "\n".join([f"`#{w.id}` **{w.created_at.strftime('%Y-%m-%d')}**: {w.reason} (By <@{w.moderator_id}>)" for w in warns])
        embed = discord.Embed(
            title=f"Warnings History for {user.display_name}",
            description=desc,
            color=0xFEE75C
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="timeout", description="Timeout (mute) a user for a duration.")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction, user: discord.Member, minutes: int, reason: str = "No reason provided."):
        duration = timedelta(minutes=minutes)
        await user.timeout(duration, reason=reason)

        async with AsyncSessionLocal() as session:
            repo = ModerationRepository(session)
            case = await repo.create_case(interaction.guild_id, user.id, interaction.user.id, "TIMEOUT", reason, int(duration.total_seconds()))

        embed = discord.Embed(
            title=f"⏰ User Timed Out (Case #{case.case_number})",
            description=f"**User:** {user.mention}\n**Duration:** {minutes} mins\n**Reason:** {reason}",
            color=0xED4245
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unmute", description="Remove timeout from a user.")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def unmute(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Timeout removed."):
        await user.timeout(None, reason=reason)

        async with AsyncSessionLocal() as session:
            repo = ModerationRepository(session)
            await repo.create_case(interaction.guild_id, user.id, interaction.user.id, "UNMUTE", reason)

        await interaction.response.send_message(f"✅ Removed timeout from {user.mention}.")

    @app_commands.command(name="kick", description="Kick a member from the server.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided."):
        await user.kick(reason=reason)

        async with AsyncSessionLocal() as session:
            repo = ModerationRepository(session)
            case = await repo.create_case(interaction.guild_id, user.id, interaction.user.id, "KICK", reason)

        embed = discord.Embed(
            title=f"👢 Member Kicked (Case #{case.case_number})",
            description=f"**User:** {user.display_name}\n**Reason:** {reason}",
            color=0xED4245
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ban", description="Ban a member from the server.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided."):
        await user.ban(reason=reason)

        async with AsyncSessionLocal() as session:
            repo = ModerationRepository(session)
            case = await repo.create_case(interaction.guild_id, user.id, interaction.user.id, "BAN", reason)

        embed = discord.Embed(
            title=f"🔨 Member Banned (Case #{case.case_number})",
            description=f"**User:** {user.display_name}\n**Reason:** {reason}",
            color=0xED4245
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="softban", description="Ban and immediately unban to clear recent messages.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def softban(self, interaction: discord.Interaction, user: discord.Member, reason: str = "Softban message cleanup."):
        await user.ban(reason=reason, delete_message_days=1)
        await interaction.guild.unban(user, reason="Softban completion")

        async with AsyncSessionLocal() as session:
            repo = ModerationRepository(session)
            case = await repo.create_case(interaction.guild_id, user.id, interaction.user.id, "SOFTBAN", reason)

        await interaction.response.send_message(f"🧹 Softbanned {user.display_name} (Case #{case.case_number}).")

    @app_commands.command(name="unban", description="Unban a user by ID.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: str, reason: str = "Unbanned by moderator."):
        try:
            uid = int(user_id)
            user_obj = await self.bot.fetch_user(uid)
            await interaction.guild.unban(user_obj, reason=reason)

            async with AsyncSessionLocal() as session:
                repo = ModerationRepository(session)
                case = await repo.create_case(interaction.guild_id, uid, interaction.user.id, "UNBAN", reason)

            await interaction.response.send_message(f"✅ Unbanned user ID {uid} (Case #{case.case_number}).")
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to unban: {e}", ephemeral=True)

    @app_commands.command(name="cases", description="View all moderation cases for a user.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def cases(self, interaction: discord.Interaction, user: discord.Member):
        async with AsyncSessionLocal() as session:
            repo = ModerationRepository(session)
            user_cases = await repo.get_user_cases(interaction.guild_id, user.id)

        if not user_cases:
            await interaction.response.send_message(f"No moderation cases found for {user.mention}.", ephemeral=True)
            return

        desc = "\n".join([f"**Case #{c.case_number}** [{c.action}] - {c.reason} (<@{c.moderator_id}>)" for c in user_cases[:10]])
        embed = discord.Embed(
            title=f"Moderation Cases for {user.display_name}",
            description=desc,
            color=0x5865F2
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(ModerationCog(bot))
