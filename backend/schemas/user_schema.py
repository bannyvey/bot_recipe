from typing import Optional, ClassVar
from pydantic import Field

from backend.mixins.database_mixin import BaseModelDatabaseMixin
from backend.models.user_model import UserModel
from backend.schemas.base import BaseModel as BaseSchema, BaseModel


class UserBase(BaseModel):
    model: ClassVar[type[UserModel]] = UserModel

    is_active: bool = Field(default=True)


class UserCreateRequest(UserBase):
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class User(UserBase, BaseModelDatabaseMixin):
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

