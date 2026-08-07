"""
Community Management Cog for Aria.
Handles FAQ search, announcements, and community events.
"""
import discord
from discord.ext import commands
from discord import app_commands


FAQS = {
    "what is opendroid": "OpenDroid is an open-source AI and software engineering community dedicated to building modern tools and bots.",
    "how to contribute": "You can contribute by checking out our GitHub repository, picking up open issues, and submitting a Pull Request!",
    "rules": "Please treat all members with respect, refrain from spamming, and follow Discord Terms of Service.",
    "ai assistant": "Aria AI supports multi-provider models including OpenAI, Anthropic, Gemini, Groq, and local Ollama!"
}


class CommunityCog(commands.Cog, name="Community"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="faq", description="Search or view community FAQ topics.")
    async def faq(self, interaction: discord.Interaction, query: str = None):
        if not query:
            topics = "\n".join([f"• `{key}`" for key in FAQS.keys()])
            embed = discord.Embed(
                title="❓ OpenDroid FAQ Topics",
                description=f"Available topics:\n{topics}\n\nType `/faq query:<topic>` for details.",
                color=0x5865F2
            )
            await interaction.response.send_message(embed=embed)
            return

        query_clean = query.lower().strip()
        answer = FAQS.get(query_clean)
        if answer:
            embed = discord.Embed(
                title=f"❓ FAQ: {query.title()}",
                description=answer,
                color=0x57F287
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"❌ Topic `{query}` not found in FAQ.", ephemeral=True)

    @app_commands.command(name="announce", description="Broadcast an official server announcement.")
    @app_commands.checks.has_permissions(administrator=True)
    async def announce(self, interaction: discord.Interaction, channel: discord.TextChannel, title: str, message: str):
        embed = discord.Embed(
            title=f"📢 {title}",
            description=message,
            color=0x5865F2
        )
        embed.set_footer(text=f"Announcement by {interaction.user.display_name} • OpenDroid")
        await channel.send(embed=embed)
        await interaction.response.send_message(f"✅ Announcement posted to {channel.mention}!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(CommunityCog(bot))
