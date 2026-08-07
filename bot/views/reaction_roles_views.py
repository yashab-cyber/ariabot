"""
Reaction Roles UI Views (Buttons & Dropdowns).
"""
import discord
from discord.ui import View, Button, Select


class ReactionRoleSelect(Select):
    def __init__(self, roles: list[discord.Role]):
        options = [
            discord.SelectOption(label=role.name, value=str(role.id), emoji="🏷️")
            for role in roles[:25]
        ]
        super().__init__(
            placeholder="Select a role to toggle...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="reaction_role_select"
        )

    async def callback(self, interaction: discord.Interaction):
        role_id = int(self.values[0])
        role = interaction.guild.get_role(role_id)
        if not role:
            await interaction.response.send_message("Role not found.", ephemeral=True)
            return

        user = interaction.user
        if role in user.roles:
            await user.remove_roles(role, reason="Reaction Role toggle")
            await interaction.response.send_message(f"➖ Removed role **{role.name}**.", ephemeral=True)
        else:
            await user.add_roles(role, reason="Reaction Role toggle")
            await interaction.response.send_message(f"➕ Added role **{role.name}**.", ephemeral=True)


class ReactionRolesView(View):
    def __init__(self, roles: list[discord.Role]):
        super().__init__(timeout=None)
        self.add_item(ReactionRoleSelect(roles))
