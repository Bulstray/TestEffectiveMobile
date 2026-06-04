from redis.asyncio import Redis

from core.config import settings
from core.shemas import UserRead

from .abstract import AbstractTokenHelper


class RedisTokensHelper(AbstractTokenHelper):
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
    ) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )

    async def create_token(self, user: UserRead) -> str:
        token = self.generate_token()
        await self.redis.set(
            token,
            user.model_dump_json(),
            ex=48000,
        )

        return token

    async def get_user_by_token(self, token: str) -> UserRead | None:
        if answer := await self.redis.get(token):
            return UserRead.model_validate_json(answer)
        return None

    async def update_user(self, token: str, user: UserRead) -> None:
        await self.redis.set(
            token,
            user.model_dump_json(),
            ex=48000,
        )

    async def delete_token(self, token: str) -> None:
        await self.redis.delete(token)


redis_tokens = RedisTokensHelper(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.tokens,
)
