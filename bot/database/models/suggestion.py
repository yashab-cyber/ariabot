"""
Suggestion ORM Model.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, String, Text, Integer, DateTime, func, JSON
from sqlalchemy.orm import Mapped, mapped_column
from bot.database.connection import Base


class Suggestion(Base):
    __tablename__ = "suggestions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(BigInteger, index=True)
    author_id: Mapped[int] = mapped_column(BigInteger, index=True)
    message_id: Mapped[int] = mapped_column(BigInteger, index=True)
    content: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="Pending") # Pending, Approved, Rejected, Under Review, Implemented, Duplicate
    upvotes: Mapped[list] = mapped_column(JSON, default=list) # List of user IDs
    downvotes: Mapped[list] = mapped_column(JSON, default=list) # List of user IDs
    staff_response: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
