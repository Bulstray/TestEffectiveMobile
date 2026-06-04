from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.shemas import UserRead
from storage.redis.users.crud import redis_tokens

static_api_token = HTTPBearer(
    auto_error=False,
    scheme_name="Static API Token",
    description="Your Static API Token from the developer portal",
)


async def validate_api_token(
    api_token: HTTPAuthorizationCredentials,
) -> UserRead:
    if answer := await redis_tokens.get_user_by_token(api_token.credentials):
        return answer

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API token",
    )


async def get_current_user(
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ],
) -> UserRead:

    if api_token:
        return await validate_api_token(api_token)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
    )
