from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixin.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .user import User


class UserSettings(IntIdPkMixin, Base):
    __tablename__ = "user_settings"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        index=True,
    )

    can_see_users: Mapped[bool] = mapped_column(
        default=True,
        server_default=true(),
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="settings",
    )
