"""
Guild Configuration ORM Model.
"""
from typing import Optional
from sqlalchemy import BigInteger, String, Boolean, Text, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column
from bot.database.connection import Base


class GuildConfig(Base):
    __tablename__ = "guild_configs"

    guild_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    prefix: Mapped[str] = mapped_column(String(10), default="!")
    
    # Feature Modules Enabled/Disabled
    ai_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    moderation_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    welcome_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    tickets_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    verification_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    leveling_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    economy_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    suggestions_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    polls_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    reminders_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    logging_enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    # Channel Configurations
    welcome_channel_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    goodbye_channel_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    mod_log_channel_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    audit_log_channel_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    ticket_category_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    suggestion_channel_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    announcement_channel_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)

    # Roles Configurations
    auto_role_ids: Mapped[list] = mapped_column(JSON, default=list)
    muted_role_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    verified_role_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    mod_role_ids: Mapped[list] = mapped_column(JSON, default=list)
    admin_role_ids: Mapped[list] = mapped_column(JSON, default=list)

    # Welcome Customization
    welcome_message: Mapped[str] = mapped_column(Text, default="Welcome {user} to {server}!")
    welcome_embed_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    auto_dm_welcome: Mapped[bool] = mapped_column(Boolean, default=False)

    # Verification System Settings
    verification_type: Mapped[str] = mapped_column(String(20), default="button") # button, captcha
    min_account_age_days: Mapped[int] = mapped_column(Integer, default=0)
    require_avatar: Mapped[bool] = mapped_column(Boolean, default=False)

    # AutoMod Settings
    automod_spam: Mapped[bool] = mapped_column(Boolean, default=True)
    automod_invite_links: Mapped[bool] = mapped_column(Boolean, default=True)
    automod_bad_words: Mapped[bool] = mapped_column(Boolean, default=False)
    automod_mass_mentions: Mapped[int] = mapped_column(Integer, default=5) # Max mentions allowed
    automod_emoji_limit: Mapped[int] = mapped_column(Integer, default=10)
    bad_words_list: Mapped[list] = mapped_column(JSON, default=list)

    # AI Model Settings
    ai_provider: Mapped[str] = mapped_column(String(30), default="openai")
    ai_model: Mapped[str] = mapped_column(String(50), default="gpt-4o-mini")
    ai_system_prompt: Mapped[str] = mapped_column(Text, default="You are Aria, a helpful Discord AI assistant for the OpenDroid community.")
