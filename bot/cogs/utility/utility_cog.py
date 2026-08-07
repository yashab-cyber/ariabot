"""
Utility Commands Cog for Aria.
Includes system stats, ping, userinfo, serverinfo, help, avatar, banner.
"""
import sys
import time
import platform
import psutil
import discord
from discord.ext import commands
from discord import app_commands
from bot.views.pagination_views import PaginationView


class UtilityCog(commands.Cog, name="Utility"):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @app_commands.command(name="ping", description="Check bot latency and API connection status.")
    async def ping(self, interaction: discord.Interaction):
        latency_ms = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"**WebSocket Latency:** `{latency_ms} ms`",
            color=0x57F287 if latency_ms < 150 else 0xFEE75C
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="botinfo", description="View statistics and technical information about Aria.")
    async def botinfo(self, interaction: discord.Interaction):
        uptime_seconds = int(time.time() - self.start_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent

        embed = discord.Embed(
            title="🤖 Aria — AI Discord Assistant",
            description="Official AI Assistant for OpenDroid Community built with Python 3.12 & discord.py 2.x.",
            color=0x5865F2
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.add_field(name="Guilds", value=f"`{len(self.bot.guilds)}`", inline=True)
        embed.add_field(name="Latency", value=f"`{round(self.bot.latency * 1000)} ms`", inline=True)
        embed.add_field(name="Uptime", value=f"`{hours}h {minutes}m {seconds}s`", inline=True)
        embed.add_field(name="Python", value=f"`{platform.python_version()}`", inline=True)
        embed.add_field(name="CPU Usage", value=f"`{cpu_usage}%`", inline=True)
        embed.add_field(name="RAM Usage", value=f"`{ram_usage}%`", inline=True)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="userinfo", description="Display detailed information about a server member.")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        target = member or interaction.user
        roles = [r.mention for r in target.roles if r != interaction.guild.default_role]

        embed = discord.Embed(
            title=f"👤 User Info — {target.display_name}",
            color=target.color if target.color.value != 0 else 0x5865F2
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(name="Username", value=f"`{target.name}`", inline=True)
        embed.add_field(name="ID", value=f"`{target.id}`", inline=True)
        embed.add_field(name="Bot Account", value=f"`{'Yes' if target.bot else 'No'}`", inline=True)
        embed.add_field(name="Account Created", value=f"<t:{int(target.created_at.timestamp())}:R>", inline=True)
        embed.add_field(name="Joined Server", value=f"<t:{int(target.joined_at.timestamp())}:R>" if target.joined_at else "N/A", inline=True)
        embed.add_field(name=f"Roles ({len(roles)})", value=" ".join(roles[:10]) if roles else "None", inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverinfo", description="Display detailed server information.")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(
            title=f"🏰 Server Info — {guild.name}",
            color=0x5865F2
        )
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="Owner", value=f"<@{guild.owner_id}>", inline=True)
        embed.add_field(name="Members", value=f"`{guild.member_count}`", inline=True)
        embed.add_field(name="Channels", value=f"`{len(guild.channels)}`", inline=True)
        embed.add_field(name="Roles", value=f"`{len(guild.roles)}`", inline=True)
        embed.add_field(name="Created At", value=f"<t:{int(guild.created_at.timestamp())}:R>", inline=True)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="help", description="View all available commands grouped by module.")
    async def help(self, interaction: discord.Interaction):
        embed1 = discord.Embed(
            title="🤖 Aria Command Directory (Page 1/2)",
            description="**AI Assistant**\n`/ask`, `/chat`, `/explain`, `/debug`, `/fix`, `/review`, `/code`, `/translate`, `/summarize`, `/rewrite`, `/grammar`, `/brainstorm`, `/ai_reset`\n\n**Moderation**\n`/warn`, `/warnings`, `/timeout`, `/unmute`, `/kick`, `/ban`, `/softban`, `/unban`, `/cases`",
            color=0x5865F2
        )

        embed2 = discord.Embed(
            title="🤖 Aria Command Directory (Page 2/2)",
            description="**Community & Management**\n`/setup_welcome`, `/setup_verification`, `/setup_tickets`, `/poll`, `/suggest`, `/setup_suggestions`, `/faq`, `/announce`\n\n**Leveling & Economy & Fun**\n`/rank`, `/leaderboard`, `/balance`, `/daily`, `/coinflip`, `/remind`, `/reminders`, `/meme`, `/8ball`, `/dice`, `/joke`",
            color=0x5865F2
        )

        view = PaginationView(embeds=[embed1, embed2], author_id=interaction.user.id)
        await interaction.response.send_message(embed=embed1, view=view)


async def setup(bot):
    await bot.add_cog(UtilityCog(bot))
