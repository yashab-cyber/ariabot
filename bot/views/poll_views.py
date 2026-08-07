"""
Poll Views: Dynamic interactive poll button view.
"""
from typing import List, Dict
import discord
from discord.ui import View, Button


class PollView(View):
    def __init__(self, options: List[str], anonymous: bool = False):
        super().__init__(timeout=None)
        self.options = options
        self.anonymous = anonymous
        # Mapping option_index -> set of user_ids
        self.votes: Dict[int, set[int]] = {i: set() for i in range(len(options))}

        for idx, option in enumerate(options):
            button = Button(
                label=f"{option} (0)",
                style=discord.ButtonStyle.secondary,
                custom_id=f"poll_opt_{idx}"
            )
            button.callback = self._make_callback(idx)
            self.add_item(button)

    def _make_callback(self, idx: int):
        async def callback(interaction: discord.Interaction):
            user_id = interaction.user.id
            # Toggle vote: remove from all other options, toggle this option
            for opt_idx, voter_set in self.votes.items():
                if opt_idx == idx:
                    if user_id in voter_set:
                        voter_set.remove(user_id)
                    else:
                        voter_set.add(user_id)
                else:
                    voter_set.discard(user_id)

            # Update buttons label
            total_votes = sum(len(s) for s in self.votes.values())
            for i, child in enumerate(self.children):
                if isinstance(child, Button):
                    count = len(self.votes[i])
                    pct = (count / total_votes * 100) if total_votes > 0 else 0
                    child.label = f"{self.options[i]} ({count} - {pct:.0f}%)"

            await interaction.response.edit_message(view=self)

        return callback
