"""
Leveling Cog for Aria.
Grants chat XP, tracks levels, and displays rank cards & leaderboards.
"""
import discord
from discord.ext import commands
from discord import app_commands
from bot.database.connection import AsyncSessionLocal
from bot.database.repositories.leveling_repo import LevelingRepository
from bot.database.repositories.guild_repo import GuildRepository


class LevelingCog(commands.Cog, name="Leveling"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        async with AsyncSessionLocal() as session:
            guild_repo = GuildRepository(session)
            config = await guild_repo.get_or_create(message.guild.id)
            if not config.leveling_enabled:
                return

            repo = LevelingRepository(session)
            user, leveled_up = await repo.add_xp(message.guild.id, message.author.id, xp_amount=15)

            if leveled_up:
                embed = discord.Embed(
                    title="🎉 Level Up!",
                    description=f"Congratulations {message.author.mention}! You reached **Level {user.level}**!",
                    color=0x57F287
                )
                await message.channel.send(embed=embed, delete_after=10)

    @app_commands.command(name="rank", description="View your or another user's current rank & level.")
    async def rank(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user

        async with AsyncSessionLocal() as session:
            repo = LevelingRepository(session)
            user_data = await repo.get_or_create_user(interaction.guild_id, target.id)

        next_level_xp = int(100 * ((user_data.level + 1) ** 1.5))
        progress_pct = min(100, int((user_data.xp / next_level_xp) * 100)) if next_level_xp > 0 else 100

        embed = discord.Embed(
            title=f"📊 Rank Card — {target.display_name}",
            color=0x5865F2
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(name="Level", value=f"**{user_data.level}**", inline=True)
        embed.add_field(name="XP", value=f"**{user_data.xp} / {next_level_xp}**", inline=True)
        embed.add_field(name="Prestige", value=f"**{user_data.prestige}**", inline=True)
        embed.add_field(name="Progress", value=f"`[{'█' * (progress_pct // 10)}{'░' * (10 - (progress_pct // 10))}] {progress_pct}%`", inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="leaderboard", description="View the server XP leaderboard.")
    async def leaderboard(self, interaction: discord.Interaction):
        async with AsyncSessionLocal() as session:
            repo = LevelingRepository(session)
            top_users = await repo.get_leaderboard(interaction.guild_id, limit=10)

        if not top_users:
            await interaction.response.send_message("No rank data available yet.", ephemeral=True)
            return

        lines = []
        for idx, u in enumerate(top_users, 1):
            member = interaction.guild.get_member(u.user_id)
            name = member.display_name if member else f"User ID {u.user_id}"
            lines.append(f"**#{idx}** {name} — Level {u.level} ({u.xp} XP)")

        embed = discord.Embed(
            title=f"🏆 Server Leaderboard — {interaction.guild.name}",
            description="\n".join(lines),
            color=0xFEE75C
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="prestige", description="Reset level 50+ to earn +1 Prestige rank!")
    async def prestige(self, interaction: discord.Interaction):
        async with AsyncSessionLocal() as session:
            repo = LevelingRepository(session)
            user_data = await repo.get_or_create_user(interaction.guild_id, interaction.user.id)

            if user_data.level < 50:
                await interaction.response.send_message("❌ You must reach **Level 50** before you can prestige.", ephemeral=True)
                return

            user_data.level = 0
            user_data.xp = 0
            user_data.prestige += 1
            await session.commit()

        embed = discord.Embed(
            title="✨ Prestige Unlocked!",
            description=f"Congratulations {interaction.user.mention}! Your level has reset and you earned **Prestige Rank #{user_data.prestige}**!",
            color=0x9B59B6
        )
        await interaction.response.send_message(embed=embed)



async def setup(bot):
    await bot.add_cog(LevelingCog(bot))
