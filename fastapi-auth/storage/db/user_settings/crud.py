from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import UserSettings


async def get_settings_for_user(
    session: AsyncSession,
    user_id: int,
) -> UserSettings | None:
    stmt = select(UserSettings).where(
        UserSettings.user_id == user_id,
    )

    result = await session.execute(stmt)
    return result.scalar_one_or_none()
