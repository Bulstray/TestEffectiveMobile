from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.shemas import UserRegistration, UserUpdate


async def get_all_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return list(result.all())


async def get_user_by_email(session: AsyncSession, email: str) -> None | User:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(
    session: AsyncSession,
    user_registration: UserRegistration,
) -> User:
    user = User(
        **user_registration.model_dump(
            exclude={"password_confirm"},
        ),
    )
    session.add(user)
    await session.commit()

    return user


async def update_user(
    session: AsyncSession,
    user_id: int,
    user_update: UserUpdate | dict[str, bool],
) -> None:
    if isinstance(user_update, UserUpdate):
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(
                **user_update.model_dump(
                    exclude_none=True,
                    exclude={"password_confirm"},
                ),
            )
        )
    else:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(
                **user_update,
            )
        )
    await session.execute(stmt)
    await session.commit()
