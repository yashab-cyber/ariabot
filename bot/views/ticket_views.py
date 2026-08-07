"""
Discord Views for Ticket System.
"""
import discord
from discord.ui import View, Button, Select, Modal, TextInput
from bot.database.connection import AsyncSessionLocal
from bot.database.repositories.ticket_repo import TicketRepository
from bot.services.transcript_service import transcript_service
from bot.utils.logger import logger


class TicketRatingModal(Modal, title="Rate Support Experience"):
    rating = TextInput(label="Rating (1-5)", placeholder="5", min_length=1, max_length=1)
    feedback = TextInput(label="Feedback (Optional)", style=discord.TextStyle.paragraph, required=False)

    def __init__(self, ticket_id: int):
        super().__init__()
        self.ticket_id = ticket_id

    async def on_submit(self, interaction: discord.Interaction):
        try:
            val = int(self.rating.value)
            if not 1 <= val <= 5:
                raise ValueError
        except ValueError:
            await interaction.response.send_message("Please provide a rating number between 1 and 5.", ephemeral=True)
            return

        async with AsyncSessionLocal() as session:
            repo = TicketRepository(session)
            ticket = await repo.get(self.ticket_id)
            if ticket:
                ticket.rating = val
                ticket.rating_feedback = self.feedback.value
                await session.commit()

        await interaction.response.send_message("Thank you for your feedback!", ephemeral=True)


class TicketActionView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Claim Ticket", style=discord.ButtonStyle.primary, custom_id="ticket_claim", emoji="⚡")
    async def claim_ticket(self, interaction: discord.Interaction, button: Button):
        async with AsyncSessionLocal() as session:
            repo = TicketRepository(session)
            ticket = await repo.get_by_channel(interaction.channel_id)
            if not ticket:
                await interaction.response.send_message("Ticket record not found.", ephemeral=True)
                return

            if ticket.claimed_by:
                await interaction.response.send_message(f"This ticket is already claimed by <@{ticket.claimed_by}>.", ephemeral=True)
                return

            ticket.claimed_by = interaction.user.id
            ticket.status = "claimed"
            await session.commit()

        embed = discord.Embed(
            description=f"✅ Ticket claimed by {interaction.user.mention}.",
            color=0x57F287
        )
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.danger, custom_id="ticket_close", emoji="🔒")
    async def close_ticket(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Closing ticket and archiving transcript...", ephemeral=True)

        channel: discord.TextChannel = interaction.channel
        messages = [m async for m in channel.history(limit=500, oldest_first=True)]
        html_content = await transcript_service.generate_html(channel, messages)

        # Close in repo
        async with AsyncSessionLocal() as session:
            repo = TicketRepository(session)
            ticket = await repo.close_ticket(channel.id)
            ticket_id = ticket.id if ticket else 0

        # Send rating prompt to ticket creator before deleting channel
        if ticket:
            creator = interaction.guild.get_member(ticket.user_id)
            if creator:
                try:
                    file = discord.File(fp=discord.io.BytesIO(html_content.encode("utf-8")), filename=f"{channel.name}-transcript.html")
                    await creator.send(f"Your ticket `{channel.name}` has been closed. Here is your transcript:", file=file)
                except Exception:
                    pass

        await channel.delete(reason=f"Ticket closed by {interaction.user.display_name}")


class TicketCategorySelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="General Support", description="Get help with general community questions", emoji="❓"),
            discord.SelectOption(label="Technical Support", description="Report bugs or technical issues", emoji="💻"),
            discord.SelectOption(label="Billing & Subscriptions", description="Questions regarding payments or perks", emoji="💳"),
            discord.SelectOption(label="Report Member/Staff", description="Report rule violations privately", emoji="🛡️"),
        ]
        super().__init__(placeholder="Select a support category...", min_values=1, max_values=1, options=options, custom_id="ticket_category_select")

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        guild = interaction.guild
        user = interaction.user

        # Create ticket channel under category or root
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{user.name[:10]}",
            overwrites=overwrites,
            reason=f"Support ticket created by {user.display_name}"
        )

        async with AsyncSessionLocal() as session:
            repo = TicketRepository(session)
            ticket = await repo.create_ticket(
                guild_id=guild.id,
                user_id=user.id,
                channel_id=channel.id,
                category=category
            )

        embed = discord.Embed(
            title=f"Support Ticket ({category})",
            description=f"Welcome {user.mention}! Support team will be with you shortly.\nPlease describe your issue in detail.",
            color=0x5865F2
        )
        embed.set_footer(text=f"ID: {ticket.ticket_id_str}")

        await channel.send(content=user.mention, embed=embed, view=TicketActionView())
        await interaction.response.send_message(f"✅ Ticket created: {channel.mention}", ephemeral=True)


class TicketLaunchView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketCategorySelect())
