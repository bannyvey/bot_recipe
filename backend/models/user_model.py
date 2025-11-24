from typing import Optional, List

from sqlalchemy import BigInteger
from sqlalchemy.orm import mapped_column, Mapped, relationship

from backend.core.database import Base


class UserModel(Base):
    __tablename__ = 'users'
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    recipe: Mapped[List["RecipeModel"]] = relationship(
        "RecipeModel",
        back_populates="user",
        cascade="all, delete, delete-orphan"
    )
