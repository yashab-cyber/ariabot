"""
Suggestion Views: Upvote/Downvote buttons and Staff Response Select/Modal.
"""
import discord
from discord.ui import View, Button
from bot.database.connection import AsyncSessionLocal
from bot.database.repositories.base import BaseRepository
from bot.database.models.suggestion import Suggestion


class SuggestionView(View):
    def __init__(self, suggestion_id: int, upvote_count: int = 0, downvote_count: int = 0):
        super().__init__(timeout=None)
        self.suggestion_id = suggestion_id

        self.up_button = Button(
            label=f"👍 {upvote_count}",
            style=discord.ButtonStyle.success,
            custom_id=f"sug_up_{suggestion_id}"
        )
        self.down_button = Button(
            label=f"👎 {downvote_count}",
            style=discord.ButtonStyle.danger,
            custom_id=f"sug_down_{suggestion_id}"
        )

        self.up_button.callback = self.upvote_callback
        self.down_button.callback = self.downvote_callback

        self.add_item(self.up_button)
        self.add_item(self.down_button)

    async def upvote_callback(self, interaction: discord.Interaction):
        await self._handle_vote(interaction, is_upvote=True)

    async def downvote_callback(self, interaction: discord.Interaction):
        await self._handle_vote(interaction, is_upvote=False)

    async def _handle_vote(self, interaction: discord.Interaction, is_upvote: bool):
        async with AsyncSessionLocal() as session:
            repo = BaseRepository(Suggestion, session)
            sug = await repo.get(self.suggestion_id)
            if not sug:
                await interaction.response.send_message("Suggestion record not found.", ephemeral=True)
                return

            user_id = interaction.user.id
            upvotes = list(sug.upvotes or [])
            downvotes = list(sug.downvotes or [])

            if is_upvote:
                if user_id in upvotes:
                    upvotes.remove(user_id)
                else:
                    upvotes.append(user_id)
                    if user_id in downvotes:
                        downvotes.remove(user_id)
            else:
                if user_id in downvotes:
                    downvotes.remove(user_id)
                else:
                    downvotes.append(user_id)
                    if user_id in upvotes:
                        upvotes.remove(user_id)

            sug.upvotes = upvotes
            sug.downvotes = downvotes
            await session.commit()

            self.up_button.label = f"👍 {len(upvotes)}"
            self.down_button.label = f"👎 {len(downvotes)}"

        await interaction.response.edit_message(view=self)
