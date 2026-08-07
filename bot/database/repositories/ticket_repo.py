"""
Ticket Repository for support ticket management.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from bot.database.models.ticket import Ticket
from bot.database.repositories.base import BaseRepository


class TicketRepository(BaseRepository[Ticket]):
    def __init__(self, session: AsyncSession):
        super().__init__(Ticket, session)

    async def create_ticket(
        self,
        guild_id: int,
        user_id: int,
        channel_id: int,
        category: str = "General Support"
    ) -> Ticket:
        stmt = select(func.count(Ticket.id)).where(Ticket.guild_id == guild_id)
        res = await self.session.execute(stmt)
        count = (res.scalar() or 0) + 1
        ticket_str = f"ticket-{count:04d}"

        ticket = Ticket(
            ticket_id_str=ticket_str,
            guild_id=guild_id,
            user_id=user_id,
            channel_id=channel_id,
            category=category,
            status="open"
        )
        self.session.add(ticket)
        await self.session.commit()
        await self.session.refresh(ticket)
        return ticket

    async def get_by_channel(self, channel_id: int) -> Optional[Ticket]:
        stmt = select(Ticket).where(Ticket.channel_id == channel_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def close_ticket(
        self,
        channel_id: int,
        transcript_url: Optional[str] = None
    ) -> Optional[Ticket]:
        ticket = await self.get_by_channel(channel_id)
        if ticket:
            ticket.status = "closed"
            ticket.closed_at = datetime.utcnow()
            if transcript_url:
                ticket.transcript_url = transcript_url
            await self.session.commit()
            await self.session.refresh(ticket)
        return ticket
