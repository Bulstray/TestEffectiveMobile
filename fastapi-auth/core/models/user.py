from sqlalchemy import Boolean, String, false, true
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixin.created_at import CreatedAtMixin
from .mixin.int_id_pk import IntIdPkMixin


class User(IntIdPkMixin, CreatedAtMixin, Base):
    __tablename__ = "users"

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

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=false(),
        nullable=False,
    )
