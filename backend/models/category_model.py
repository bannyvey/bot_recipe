from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base


class CategoryModel(Base):
    __tablename__ = 'categories'
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=False)

    recipe: Mapped[list["RecipeModel"]] = relationship(
        "RecipeModel", back_populates="category", cascade="all, delete, delete-orphan"
    )
