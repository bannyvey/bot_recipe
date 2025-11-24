from typing import Optional

from sqlalchemy import ForeignKey, UniqueConstraint, Index, text, or_
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base


class RecipeModel(Base):
    __tablename__ = 'recipes'
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    ingredients: Mapped[str] = mapped_column(nullable=False)
    cooking_time: Mapped[Optional[int]] = mapped_column(nullable=False)
    complexity: Mapped[Optional[int]] = mapped_column(nullable=False)

    admin_approved: Mapped[bool] = mapped_column(default=False)
    user_approved: Mapped[bool] = mapped_column(default=False)

    telegram_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id', ondelete="CASCADE"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete="CASCADE"), nullable=False)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="recipe")
    category: Mapped["CategoryModel"] = relationship("CategoryModel", back_populates="recipe")

    __table_args__ = (
        Index(
            "uq_recipes_title_approved",
            "title",
            unique=True,
            postgresql_where=text("admin_approved = true")
        ),
        Index(
            "uq_recipes_title_user_approved",
            "title", "telegram_id",
            unique=True,
            postgresql_where=text("admin_approved = false")
        )
    )
    
    @classmethod
    def get_cond_list(cls, **kwargs) -> list:
        """Получить список условий для фильтрации рецептов"""
        from sqlalchemy import and_
        
        cond_list = []
        
        # Фильтр по категории
        if kwargs.get("category_id"):
            cond_list.append(cls.category_id == kwargs["category_id"])
        
        # Фильтр по сложности
        if kwargs.get("difficulty"):
            cond_list.append(cls.difficulty == kwargs["difficulty"])
        
        # Фильтр по максимальному времени приготовления
        if kwargs.get("cooking_time_max"):
            cond_list.append(cls.cooking_time <= kwargs["cooking_time_max"])
        
        # Фильтр по минимальному времени приготовления
        if kwargs.get("cooking_time_min"):
            cond_list.append(cls.cooking_time >= kwargs["cooking_time_min"])
        
        # Поиск по тексту
        if kwargs.get("search"):
            search_term = f"%{kwargs['search'].lower()}%"
            cond_list.append(
                or_(
                    cls.title.ilike(search_term),
                    cls.description.ilike(search_term),
                    cls.ingredients.ilike(search_term)
                )
            )
        
        # Фильтр по статусу одобрения администратором
        if kwargs.get("admin_approved") is not None:
            cond_list.append(cls.admin_approved == kwargs["admin_approved"])
        
        # Фильтр по статусу одобрения пользователем
        if kwargs.get("user_approved") is not None:
            cond_list.append(cls.user_approved == kwargs["user_approved"])
        
        # Фильтр по пользователю
        if kwargs.get("user_id"):
            cond_list.append(cls.user_id == kwargs["user_id"])
        
        # Исключаем удаленные записи
        cond_list.append(cls.is_deleted == False)
        
        return cond_list

    @classmethod
    def get_cond_list(cls, **kwargs) -> list:
        """Получить список условий для фильтрации (переопределяется в наследниках)"""
        data = []
        for field, value in kwargs.items():
            column = getattr(cls, field)
            data.append(column==value)

        return data
