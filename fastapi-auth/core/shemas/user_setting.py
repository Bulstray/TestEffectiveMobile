from pydantic import BaseModel


class UserSettingsBase(BaseModel):
    can_see_users: bool = True


class UserSettingsUpdate(UserSettingsBase):
    """Модель для обновления данных"""
