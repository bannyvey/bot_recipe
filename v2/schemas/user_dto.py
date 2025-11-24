from typing import Optional

from pydantic import BaseModel


class UserFindId(BaseModel):
    telegram_id: str

class UserId(BaseModel):
    id: int

class UserCreateDTO(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserDTO(BaseModel):
    id: int
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
