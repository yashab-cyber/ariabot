"""
User Profile ORM Model.
"""
from typing import Optional
from sqlalchemy import BigInteger, String, JSON, Integer, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from bot.database.connection import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    preferred_ai_provider: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    preferred_ai_model: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    timezone: Mapped[str] = mapped_column(String(50), default="UTC")
    ai_memory: Mapped[dict] = mapped_column(JSON, default=dict)
    total_ai_tokens_used: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
