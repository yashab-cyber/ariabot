"""
Pagination View: Allows navigating through multi-page embeds easily.
"""
from typing import List
import discord
from discord.ui import View, Button


class PaginationView(View):
    def __init__(self, embeds: List[discord.Embed], author_id: int):
        super().__init__(timeout=180)
        self.embeds = embeds
        self.author_id = author_id
        self.current_page = 0

        self.update_buttons()

    def update_buttons(self):
        self.clear_items()

        prev_btn = Button(label="Previous", style=discord.ButtonStyle.secondary, emoji="◀️", disabled=self.current_page == 0)
        prev_btn.callback = self.prev_page
        self.add_item(prev_btn)

        page_btn = Button(label=f"Page {self.current_page + 1}/{len(self.embeds)}", style=discord.ButtonStyle.primary, disabled=True)
        self.add_item(page_btn)

        next_btn = Button(label="Next", style=discord.ButtonStyle.secondary, emoji="▶️", disabled=self.current_page == len(self.embeds) - 1)
        next_btn.callback = self.next_page
        self.add_item(next_btn)

    async def prev_page(self, interaction: discord.Interaction):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Only the command caller can navigate pages.", ephemeral=True)
            return

        self.current_page -= 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

    async def next_page(self, interaction: discord.Interaction):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Only the command caller can navigate pages.", ephemeral=True)
            return

        self.current_page += 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
