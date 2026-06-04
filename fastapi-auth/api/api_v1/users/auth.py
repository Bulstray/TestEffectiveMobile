from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, db_helper
from core.shemas import UserRead
from dependencies.auth import get_current_user
from dependencies.permissions import can_this_user_see_users
from storage.db.users import crud

from .dependencies import (
    create_new_account,
    logout_system,
    soft_delete_user,
    update_settings,
    update_user_profile,
    validate_basic_auth_user,
)

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[UserRead],
)
async def get_all_users(
    _: Annotated[
        None,
        Depends(can_this_user_see_users),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> list[User]:
    return await crud.get_all_users(session)


@router.get("/me")
async def current_user(
    user: Annotated[
        UserRead,
        Depends(get_current_user),
    ],
) -> UserRead:
    return user


@router.patch("/update_user_settings")
async def update_user_settings(
    _: Annotated[
        None,
        Depends(update_settings),
    ],
) -> dict[str, str]:
    return {
        "message": "user settings updated",
    }


@router.post(
    "/registration",
    status_code=status.HTTP_201_CREATED,
)
async def registration(
    token: Annotated[
        str,
        Depends(create_new_account),
    ],
) -> str:
    return token


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
async def login(
    token_if_data_correct: Annotated[
        str,
        Depends(validate_basic_auth_user),
    ],
) -> str:
    return token_if_data_correct


@router.patch(
    "/update",
    status_code=status.HTTP_200_OK,
)
def update(
    _: Annotated[
        None,
        Depends(update_user_profile),
    ],
) -> dict[str, str]:
    return {
        "message": "User updated",
    }


@router.delete("/delete_account")
async def delete_account(
    _: Annotated[
        None,
        Depends(soft_delete_user),
    ],
) -> dict[str, str]:
    return {
        "message": "Account deleted",
    }


@router.post("/logout")
async def logout(
    _: Annotated[
        None,
        Depends(
            logout_system,
        ),
    ],
) -> dict[str, str]:
    return {
        "message": "User logout",
    }
