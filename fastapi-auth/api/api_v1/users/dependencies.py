from typing import Annotated

import bcrypt
from fastapi import Depends, Form, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.shemas import (
    UserLogin,
    UserRead,
    UserRegistration,
    UserUpdate,
)
from dependencies.auth import get_current_user, static_api_token
from dependencies.permissions import is_superuser
from storage.db.user_settings.crud import (
    create_user_settings,
    update_user_settings,
)
from storage.db.users import crud
from storage.redis.users.crud import redis_tokens


async def logout_system(
    request: Request,
    current_user: Annotated[
        UserRead,
        Depends(get_current_user),
    ],
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(static_api_token),
    ],
) -> None:
    await redis_tokens.delete_token(credentials.credentials)


async def update_settings(
    user_id: Annotated[int, Form(...)],
    can_see_users: Annotated[bool, Form(...)],
    is_admin: Annotated[
        None,
        Depends(is_superuser),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> None:

    await update_user_settings(
        session,
        user_id,
        {
            "can_see_users": can_see_users,
        },
    )


async def soft_delete_user(
    request: Request,
    current_user: Annotated[
        UserRead,
        Depends(get_current_user),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(static_api_token),
    ],
) -> None:
    await crud.update_user(
        session,
        user_id=current_user.id,
        user_update={"is_active": False},
    )
    await redis_tokens.delete_token(credentials.credentials)


async def update_user_profile(
    request: Request,
    user_update: UserUpdate,
    current_user: Annotated[
        UserRead,
        Depends(get_current_user),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(static_api_token),
    ],
) -> None:
    await crud.update_user(
        session,
        user_id=current_user.id,
        user_update=user_update,
    )

    current_user_update = current_user.model_copy(
        update=user_update.model_dump(
            exclude_none=True,
            exclude={
                "hashed_password",
                "password_confirm",
            },
        ),
    )

    await redis_tokens.update_user(
        credentials.credentials,
        current_user_update,
    )


async def create_new_account(
    request: Request,
    user_registration: UserRegistration,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> str:
    if await crud.get_user_by_email(
        session,
        f"{user_registration.email}",
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    user = await crud.create_user(
        session,
        user_registration,
    )

    user_read = UserRead.model_validate(user)

    await create_user_settings(
        session,
        user_read.id,
    )

    return await redis_tokens.create_token(user_read)


async def validate_basic_auth_user(
    request: Request,
    user_login: UserLogin,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> str:
    user_in_db = await crud.get_user_by_email(
        session,
        f"{user_login.email}",
    )

    if (
        user_in_db
        and bcrypt.checkpw(
            password=user_login.password.encode("utf-8"),
            hashed_password=user_in_db.hashed_password.encode("utf-8"),
        )
        and user_in_db.is_active
    ):
        user_read = UserRead.model_validate(user_in_db)
        return await redis_tokens.create_token(user_read)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
    )
