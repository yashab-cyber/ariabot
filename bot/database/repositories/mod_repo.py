"""
Moderation Repository for handling cases, warnings, and notes.
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from bot.database.models.moderation import ModerationCase, WarningRecord, ModNote
from bot.database.repositories.base import BaseRepository


class ModerationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_case(
        self,
        guild_id: int,
        user_id: int,
        moderator_id: int,
        action: str,
        reason: str = "No reason provided.",
        duration_seconds: Optional[int] = None
    ) -> ModerationCase:
        # Get next case number for this guild
        stmt = select(func.coalesce(func.max(ModerationCase.case_number), 0)).where(
            ModerationCase.guild_id == guild_id
        )
        result = await self.session.execute(stmt)
        next_case_num = (result.scalar() or 0) + 1

        case = ModerationCase(
            guild_id=guild_id,
            case_number=next_case_num,
            user_id=user_id,
            moderator_id=moderator_id,
            action=action,
            reason=reason,
            duration_seconds=duration_seconds,
            active=True
        )
        self.session.add(case)
        await self.session.commit()
        await self.session.refresh(case)
        return case

    async def get_user_cases(self, guild_id: int, user_id: int) -> List[ModerationCase]:
        stmt = select(ModerationCase).where(
            ModerationCase.guild_id == guild_id,
            ModerationCase.user_id == user_id
        ).order_by(ModerationCase.case_number.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def add_warning(self, guild_id: int, user_id: int, moderator_id: int, reason: str) -> WarningRecord:
        warn = WarningRecord(
            guild_id=guild_id,
            user_id=user_id,
            moderator_id=moderator_id,
            reason=reason
        )
        self.session.add(warn)
        await self.session.commit()
        await self.session.refresh(warn)
        return warn

    async def get_user_warnings(self, guild_id: int, user_id: int) -> List[WarningRecord]:
        stmt = select(WarningRecord).where(
            WarningRecord.guild_id == guild_id,
            WarningRecord.user_id == user_id
        ).order_by(WarningRecord.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def add_note(self, guild_id: int, user_id: int, author_id: int, note: str) -> ModNote:
        mod_note = ModNote(
            guild_id=guild_id,
            user_id=user_id,
            author_id=author_id,
            note=note
        )
        self.session.add(mod_note)
        await self.session.commit()
        await self.session.refresh(mod_note)
        return mod_note

    async def get_user_notes(self, guild_id: int, user_id: int) -> List[ModNote]:
        stmt = select(ModNote).where(
            ModNote.guild_id == guild_id,
            ModNote.user_id == user_id
        ).order_by(ModNote.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
