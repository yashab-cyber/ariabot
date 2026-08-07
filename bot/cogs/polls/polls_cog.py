"""
Polls Cog for Aria.
Creates interactive button-based polls.
"""
import discord
from discord.ext import commands
from discord import app_commands
from bot.views.poll_views import PollView


class PollsCog(commands.Cog, name="Polls"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="poll", description="Create an interactive poll with up to 5 options.")
    async def poll(
        self,
        interaction: discord.Interaction,
        question: str,
        option_1: str,
        option_2: str,
        option_3: str = None,
        option_4: str = None,
        option_5: str = None,
        anonymous: bool = False
    ):
        options = [opt for opt in [option_1, option_2, option_3, option_4, option_5] if opt]

        embed = discord.Embed(
            title=f"📊 Poll: {question}",
            description="Click a button below to cast or change your vote!",
            color=0x5865F2
        )
        embed.set_footer(text=f"Created by {interaction.user.display_name} • {'Anonymous' if anonymous else 'Public'}")

        view = PollView(options=options, anonymous=anonymous)
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(PollsCog(bot))
