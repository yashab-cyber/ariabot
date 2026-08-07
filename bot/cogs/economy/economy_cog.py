"""
Economy Cog for Aria.
Handles coins, daily streaks, transfers, and coin flip games.
"""
import random
import discord
from discord.ext import commands
from discord import app_commands
from bot.database.connection import AsyncSessionLocal
from bot.database.repositories.economy_repo import EconomyRepository


class EconomyCog(commands.Cog, name="Economy"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="balance", description="Check your wallet and bank balance.")
    async def balance(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        async with AsyncSessionLocal() as session:
            repo = EconomyRepository(session)
            eco_user = await repo.get_or_create(interaction.guild_id, target.id)

        embed = discord.Embed(
            title=f"💰 Balance — {target.display_name}",
            color=0xFEE75C
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(name="Wallet", value=f"🪙 `{eco_user.wallet:,}`", inline=True)
        embed.add_field(name="Bank", value=f"🏦 `{eco_user.bank:,}`", inline=True)
        embed.add_field(name="Total Net Worth", value=f"✨ `{eco_user.wallet + eco_user.bank:,}`", inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="daily", description="Claim your daily coin reward.")
    async def daily(self, interaction: discord.Interaction):
        async with AsyncSessionLocal() as session:
            repo = EconomyRepository(session)
            success, amount, msg = await repo.claim_daily(interaction.guild_id, interaction.user.id)

        color = 0x57F287 if success else 0xED4245
        embed = discord.Embed(
            title="🎁 Daily Reward",
            description=msg,
            color=color
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="coinflip", description="Bet coins on a coin flip (heads/tails).")
    async def coinflip(self, interaction: discord.Interaction, choice: str, bet: int):
        choice = choice.lower()
        if choice not in ["heads", "tails"]:
            await interaction.response.send_message("Please choose `heads` or `tails`.", ephemeral=True)
            return

        if bet <= 0:
            await interaction.response.send_message("Bet amount must be greater than 0.", ephemeral=True)
            return

        async with AsyncSessionLocal() as session:
            repo = EconomyRepository(session)
            eco_user = await repo.get_or_create(interaction.guild_id, interaction.user.id)

            if eco_user.wallet < bet:
                await interaction.response.send_message("❌ You do not have enough coins in your wallet for this bet.", ephemeral=True)
                return

            result = random.choice(["heads", "tails"])
            won = (choice == result)

            if won:
                eco_user.wallet += bet
                outcome_text = f"🎉 The coin landed on **{result.upper()}**! You won **{bet}** coins!"
                color = 0x57F287
            else:
                eco_user.wallet -= bet
                outcome_text = f"💀 The coin landed on **{result.upper()}**! You lost **{bet}** coins."
                color = 0xED4245

            await session.commit()

        embed = discord.Embed(
            title="🪙 Coin Flip Result",
            description=outcome_text,
            color=color
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(EconomyCog(bot))
