from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.shemas import UserRead
from storage.db.user_settings.crud import get_settings_for_user

from .auth import get_current_user


async def can_this_user_see_users(
    current_user: Annotated[
        UserRead,
        Depends(get_current_user),
    ],
    session: Annotated[
        AsyncSession,
        Depends(
            db_helper.session_getter,
        ),
    ],
) -> None:
    user_settings = await get_settings_for_user(session, current_user.id)

    if user_settings is not None and user_settings.can_see_users:
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You don't have access to this resource",
    )


async def is_superuser(
    current_user: Annotated[
        UserRead,
        Depends(get_current_user),
    ],
) -> None:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this resource",
        )
