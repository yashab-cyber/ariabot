"""
Fun Cog for Aria.
Entertainment, memes, games, 8ball, jokes, facts.
"""
import random
import discord
from discord.ext import commands
from discord import app_commands


EIGHT_BALL_ANSWERS = [
    "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes definitely.",
    "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.",
    "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
    "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good."
]

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "There are 10 types of people in the world: those who understand binary, and those who don't.",
    "Why did the Python programmer get lost in the woods? Because they couldn't find their indent!",
    "Hardware: The part of a computer that you can kick."
]

FACTS = [
    "Python was named after the British comedy series 'Monty Python's Flying Circus'.",
    "The first computer bug was an actual moth found in a Harvard Mark II computer in 1947.",
    "Discord was launched in May 2015 to solve communication issues for online gamers."
]


class FunCog(commands.Cog, name="Fun"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="8ball", description="Ask the Magic 8-Ball a question.")
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        answer = random.choice(EIGHT_BALL_ANSWERS)
        embed = discord.Embed(
            title="🎱 Magic 8-Ball",
            description=f"**Question:** {question}\n**Answer:** {answer}",
            color=0x9B59B6
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="dice", description="Roll a die (1-6) or custom sides.")
    async def dice(self, interaction: discord.Interaction, sides: int = 6):
        if sides < 2:
            await interaction.response.send_message("Dice must have at least 2 sides.", ephemeral=True)
            return
        roll = random.randint(1, sides)
        await interaction.response.send_message(f"🎲 You rolled a **{roll}** (d{sides}).")

    @app_commands.command(name="joke", description="Get a programming or tech joke.")
    async def joke(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"😂 {random.choice(JOKES)}")

    @app_commands.command(name="fact", description="Learn a random tech or coding fact.")
    async def fact(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"💡 **Fact:** {random.choice(FACTS)}")


async def setup(bot):
    await bot.add_cog(FunCog(bot))
