"""
Analytics ORM Models.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, String, Integer, DateTime, func, JSON
from sqlalchemy.orm import Mapped, mapped_column
from bot.database.connection import Base


class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guild_id: Mapped[Optional[int]] = mapped_column(BigInteger, index=True, nullable=True)
    event_type: Mapped[str] = mapped_column(String(50), index=True) # message, command, ai_prompt, ticket_created, mod_action, join, leave
    user_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
