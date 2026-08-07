"""
AI Assistant Cog for Aria.
Provides all AI slash commands, multi-provider execution, streaming, and context tracking.
"""
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from bot.services.ai_service import ai_service
from bot.database.connection import AsyncSessionLocal
from bot.database.repositories.base import BaseRepository
from bot.database.models.user import UserProfile
from bot.utils.logger import logger


class AICog(commands.Cog, name="AI Assistant"):
    def __init__(self, bot):
        self.bot = bot

    def _get_context_key(self, interaction: discord.Interaction) -> str:
        return f"user:{interaction.user.id}:chan:{interaction.channel_id}"

    async def _process_ai_request(
        self,
        interaction: discord.Interaction,
        prompt: str,
        system_prefix: str = "",
        ephemeral: bool = False
    ):
        await interaction.response.defer(ephemeral=ephemeral)
        ctx_key = self._get_context_key(interaction)

        full_prompt = f"{system_prefix}\n{prompt}" if system_prefix else prompt
        topic = ai_service.detect_topic(prompt)

        # Stream response chunks or send completed response
        response_text = ""
        async for chunk in ai_service.generate_response(full_prompt, context_key=ctx_key):
            response_text += chunk

        # Split into 4000 character chunks if long to prevent truncation
        chunks = [response_text[i:i+4000] for i in range(0, len(response_text), 4000)]
        for idx, chunk in enumerate(chunks):
            embed = discord.Embed(
                title=f"🤖 Aria AI — {topic}" if idx == 0 else f"🤖 Aria AI — {topic} (Cont. {idx+1})",
                description=chunk,
                color=0x5865F2
            )
            embed.set_footer(text=f"Requested by {interaction.user.display_name} • OpenDroid AI")
            await interaction.followup.send(embed=embed, ephemeral=ephemeral)


    @app_commands.command(name="ask", description="Ask Aria AI any question.")
    async def ask(self, interaction: discord.Interaction, question: str):
        await self._process_ai_request(interaction, question)

    @app_commands.command(name="chat", description="Have an interactive conversation with Aria.")
    async def chat(self, interaction: discord.Interaction, message: str):
        await self._process_ai_request(interaction, message)

    @app_commands.command(name="explain", description="Explain a concept or snippet in simple terms.")
    async def explain(self, interaction: discord.Interaction, concept: str):
        prompt = f"Explain the following concept clearly with code/examples if helpful:\n{concept}"
        await self._process_ai_request(interaction, prompt)

    @app_commands.command(name="debug", description="Analyze and debug code or stack traces.")
    async def debug(self, interaction: discord.Interaction, code_or_error: str):
        prompt = f"Identify the bugs, explain the cause, and provide fixed code:\n```\n{code_or_error}\n```"
        await self._process_ai_request(interaction, prompt)

    @app_commands.command(name="fix", description="Automatically fix errors in your code snippet.")
    async def fix(self, interaction: discord.Interaction, code: str):
        prompt = f"Fix all syntax and logical errors in this code:\n```\n{code}\n```"
        await self._process_ai_request(interaction, prompt)

    @app_commands.command(name="review", description="Provide code review feedback and best practices.")
    async def review(self, interaction: discord.Interaction, code: str):
        prompt = f"Perform a comprehensive code review focusing on performance, security, and cleanliness:\n```\n{code}\n```"
        await self._process_ai_request(interaction, prompt)

    @app_commands.command(name="code", description="Generate clean code for a specific task.")
    async def code(self, interaction: discord.Interaction, requirement: str):
        prompt = f"Write clean, production-ready code with type annotations for:\n{requirement}"
        await self._process_ai_request(interaction, prompt)

    @app_commands.command(name="translate", description="Translate text into another language.")
    async def translate(self, interaction: discord.Interaction, target_language: str, text: str):
        prompt = f"Translate the following text into {target_language}:\n{text}"
        await self._process_ai_request(interaction, prompt)

    @app_commands.command(name="summarize", description="Summarize long text or articles.")
    async def summarize(self, interaction: discord.Interaction, text: str):
        prompt = f"Provide a bulleted summary of key points for:\n{text}"
        await self._process_ai_request(interaction, prompt)

    @app_commands.command(name="rewrite", description="Rewrite text for clarity, tone, or style.")
    async def rewrite(self, interaction: discord.Interaction, text: str, tone: Optional[str] = "professional"):
        prompt = f"Rewrite the following text with a {tone} tone:\n{text}"
        await self._process_ai_request(interaction, prompt)

    @app_commands.command(name="grammar", description="Check and correct grammar and spelling.")
    async def grammar(self, interaction: discord.Interaction, text: str):
        prompt = f"Check for grammar, spelling, and punctuation errors:\n{text}"
        await self._process_ai_request(interaction, prompt)

    @app_commands.command(name="brainstorm", description="Generate creative ideas for a topic.")
    async def brainstorm(self, interaction: discord.Interaction, topic: str):
        prompt = f"Generate 5-10 innovative ideas for:\n{topic}"
        await self._process_ai_request(interaction, prompt)

    @app_commands.command(name="ai_reset", description="Reset your active AI conversation memory.")
    async def ai_reset(self, interaction: discord.Interaction):
        ctx_key = self._get_context_key(interaction)
        ai_service.clear_history(ctx_key)
        await interaction.response.send_message("🧠 Conversation memory cleared!", ephemeral=True)

    @app_commands.command(name="ai_provider", description="Set your preferred AI provider.")
    async def ai_provider(
        self,
        interaction: discord.Interaction,
        provider: str
    ):
        prov_clean = provider.lower().strip()
        valid = ["openai", "anthropic", "groq", "openrouter", "ollama", "lmstudio"]
        if prov_clean not in valid:
            await interaction.response.send_message(f"❌ Invalid provider. Choose from: `{', '.join(valid)}`", ephemeral=True)
            return

        ai_service.set_user_preference(interaction.user.id, provider=prov_clean)
        await interaction.response.send_message(f"✅ Preferred AI provider set to **{prov_clean.title()}**.", ephemeral=True)

    @app_commands.command(name="ai_model", description="Set your preferred AI model name.")
    async def ai_model(
        self,
        interaction: discord.Interaction,
        model_name: str
    ):
        ai_service.set_user_preference(interaction.user.id, model=model_name)
        await interaction.response.send_message(f"✅ Preferred AI model set to **{model_name}**.", ephemeral=True)



async def setup(bot):
    await bot.add_cog(AICog(bot))
