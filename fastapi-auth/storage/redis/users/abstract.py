import secrets
from abc import ABC, abstractmethod

from core.shemas import UserRead


class AbstractTokenHelper(ABC):
    @abstractmethod
    async def create_token(
        self,
        user: UserRead,
    ) -> str:
        """
        Save token in storage.
        :param user:
        :return:
        """

    @abstractmethod
    async def delete_token(
        self,
        token: str,
    ) -> None:
        """
        Delete token
        :param token:
        :return:
        """

    @abstractmethod
    async def get_user_by_token(
        self,
        token: str,
    ) -> UserRead | None:
        """
        User from user
        :param token:
        :return: UserRead or None
        """

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe(16)
