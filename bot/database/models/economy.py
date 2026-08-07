"""
Economy ORM Model.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, Integer, DateTime, func, JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from bot.database.connection import Base


class EconomyUser(Base):
    __tablename__ = "economy_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(BigInteger, index=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    wallet: Mapped[int] = mapped_column(Integer, default=100)
    bank: Mapped[int] = mapped_column(Integer, default=0)
    daily_streak: Mapped[int] = mapped_column(Integer, default=0)
    last_daily: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    inventory: Mapped[list] = mapped_column(JSON, default=list) # List of item dicts
    badges: Mapped[list] = mapped_column(JSON, default=list) # List of badge strings
