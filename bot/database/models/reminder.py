"""
Reminder ORM Model.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, String, Text, Integer, DateTime, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from bot.database.connection import Base


class Reminder(Base):
    __tablename__ = "reminders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    channel_id: Mapped[int] = mapped_column(BigInteger)
    guild_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    message: Mapped[str] = mapped_column(Text)
    remind_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False)
    recurrence_interval: Mapped[Optional[str]] = mapped_column(String(30), nullable=True) # daily, weekly, etc.
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
