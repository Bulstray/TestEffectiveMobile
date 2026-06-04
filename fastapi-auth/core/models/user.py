from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, false, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixin.created_at import CreatedAtMixin
from .mixin.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .user_settings import UserSettings


class User(IntIdPkMixin, CreatedAtMixin, Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(
        String(length=64),
    )

    surname: Mapped[str] = mapped_column(
        String(length=64),
    )

    patronymics: Mapped[str] = mapped_column(
        String(length=64),
    )

    email: Mapped[str] = mapped_column(
        String(320),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        server_default=true(),
    )

    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=false(),
        nullable=False,
    )

    settings: Mapped["UserSettings"] = relationship(
        "UserSettings",
        back_populates="user",
        lazy="selectin",
    )
