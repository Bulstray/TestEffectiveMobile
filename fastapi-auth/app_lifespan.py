from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import settings
from core.models import db_helper
from storage.db.user_settings.crud import create_user_settings
from storage.db.users import crud


async def create_admin() -> None:
    async with db_helper.session_factory() as session:

        if await crud.get_user_by_email(session, settings.superuser.email):
            return

        superuser = await crud.create_user(session, settings.superuser)

        await create_user_settings(session, superuser.id)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:

    await create_admin()

    yield

    await db_helper.dispose()
