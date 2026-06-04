from typing import Self

from pydantic import BaseModel, ConfigDict, EmailStr, model_validator

from utils import hash_password

PASSWORD_EMPTY = "Password cannot be empty"
PASSWORD_NOT_MATCH = "Passwords do not match"
BOTH_PASSWORD_CHANGE = "Both password fields are required when changing"


class UserBase(BaseModel):
    name: str
    surname: str
    patronymics: str
    email: EmailStr


class UserUpdate(BaseModel):
    name: str | None = None
    surname: str | None = None
    patronymics: str | None = None
    email: EmailStr | None = None
    hashed_password: str | None = None
    password_confirm: str | None = None

    @model_validator(mode="after")
    def check_password_match(self) -> Self:
        if self.hashed_password is None and self.password_confirm is None:
            return self

        if self.hashed_password is None or self.password_confirm is None:
            raise ValueError(BOTH_PASSWORD_CHANGE)

        if not self.hashed_password:
            raise ValueError(PASSWORD_EMPTY)

        if self.hashed_password != self.password_confirm:
            raise ValueError(PASSWORD_NOT_MATCH)

        self.hashed_password = hash_password(self.hashed_password)
        return self


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(UserBase):
    id: int
    is_superuser: bool = False

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserRegistration(UserBase):
    hashed_password: str
    password_confirm: str

    @model_validator(mode="after")
    def check_password_match(self) -> Self:
        if not self.hashed_password:
            raise ValueError(PASSWORD_EMPTY)

        if self.hashed_password != self.password_confirm:
            raise ValueError(PASSWORD_NOT_MATCH)

        self.hashed_password = hash_password(self.hashed_password)

        return self
