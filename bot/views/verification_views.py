"""
Verification Views: Captcha modal and verification button.
"""
import discord
from discord.ui import View, Button, Modal, TextInput
from bot.services.captcha_service import captcha_service
from bot.database.connection import AsyncSessionLocal
from bot.database.repositories.guild_repo import GuildRepository


class CaptchaVerifyModal(Modal, title="Security Captcha Verification"):
    captcha_answer = TextInput(label="Enter the code shown in image", min_length=4, max_length=6)

    def __init__(self, expected_code: str):
        super().__init__()
        self.expected_code = expected_code

    async def on_submit(self, interaction: discord.Interaction):
        if self.captcha_answer.value.strip().upper() == self.expected_code:
            # Grant verified role if configured
            async with AsyncSessionLocal() as session:
                repo = GuildRepository(session)
                config = await repo.get(interaction.guild_id)
                if config and config.verified_role_id:
                    role = interaction.guild.get_role(config.verified_role_id)
                    if role:
                        await interaction.user.add_roles(role, reason="Captcha Verification Passed")

            await interaction.response.send_message("✅ Verification successful! Access granted.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Invalid code. Please try again.", ephemeral=True)


class VerificationLaunchView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify Now", style=discord.ButtonStyle.success, custom_id="verification_verify_btn", emoji="✅")
    async def verify_button(self, interaction: discord.Interaction, button: Button):
        # Generate Captcha Image
        buffer, code = captcha_service.generate_captcha()
        file = discord.File(fp=buffer, filename="captcha.png")

        modal = CaptchaVerifyModal(expected_code=code)
        
        # Send ephemeral image preview along with prompt
        await interaction.response.send_message("Please solve the captcha code below:", file=file, ephemeral=True)
        # Note: modal must be submitted separately or triggered
