from sqlalchemy import select, update
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


async def create_user_settings(
    session: AsyncSession,
    user_id: int,
) -> None:
    session.add(
        UserSettings(user_id=user_id),
    )
    await session.commit()


async def update_user_settings(
    session: AsyncSession,
    user_id: int,
    settings: dict[str, bool],
) -> None:
    stmt = (
        update(UserSettings)
        .where(UserSettings.user_id == user_id)
        .values(
            **settings,
        )
    )

    await session.execute(stmt)
    await session.commit()
