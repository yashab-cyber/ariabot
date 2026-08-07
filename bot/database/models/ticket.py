"""
Ticket ORM Model.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, String, Text, Integer, DateTime, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from bot.database.connection import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ticket_id_str: Mapped[str] = mapped_column(String(50), unique=True, index=True) # e.g. ticket-0001
    guild_id: Mapped[int] = mapped_column(BigInteger, index=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    channel_id: Mapped[int] = mapped_column(BigInteger, index=True)
    category: Mapped[str] = mapped_column(String(50), default="General Support")
    status: Mapped[str] = mapped_column(String(20), default="open") # open, claimed, closed
    claimed_by: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    rating_feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    transcript_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
