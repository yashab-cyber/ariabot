"""
Leveling ORM Model.
"""
from datetime import datetime
from sqlalchemy import BigInteger, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from bot.database.connection import Base


class LevelUser(Base):
    __tablename__ = "level_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(BigInteger, index=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    xp: Mapped[int] = mapped_column(Integer, default=0)
    level: Mapped[int] = mapped_column(Integer, default=0)
    voice_seconds: Mapped[int] = mapped_column(Integer, default=0)
    prestige: Mapped[int] = mapped_column(Integer, default=0)
    last_xp_given: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
