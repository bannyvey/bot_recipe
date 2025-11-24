from typing import Optional, List, ClassVar
from pydantic import Field


from backend.schemas.base import BaseModel
from backend.mixins.database_mixin import BaseModelDatabaseMixin
from backend.models.recipe_model import RecipeModel


class RecipeBase(BaseModel):
    model: ClassVar[type[RecipeModel]] = RecipeModel

    title: str = Field(min_length=1, max_length=200, description="Название рецепта")
    description: Optional[str] = Field(default=None, max_length=1000, description="Описание рецепта")
    ingredients: str = Field(min_length=1, max_length=2000, description="Список ингредиентов")
    cooking_time: int = Field(gt=1, le=1440, description="Время приготовления в минутах")
    complexity: int = Field(ge=1, le=5, description="Сложность от 1 до 5")
    telegram_id: int = Field(description="ID пользователя tg")
    category_id: int = Field(ge=1, le=7, description="ID категории")



class RecipeCreate(RecipeBase):
    title: str = Field(min_length=1, max_length=200, description="Название рецепта")
    description: Optional[str] = Field(default=None, max_length=1000, description="Описание рецепта")
    ingredients: str = Field(min_length=1, max_length=2000, description="Список ингредиентов")
    cooking_time: int = Field(gt=1, le=1440, description="Время приготовления в минутах")
    complexity: int = Field(ge=1, le=5, description="Сложность от 1 до 5")
    telegram_id: int = Field(description="ID пользователя tg")
    category_id: int = Field(ge=1, le=7, description="ID категории")


class Recipe(RecipeBase, BaseModelDatabaseMixin):
    id: int = Field(description="ID рецепта")


class RecipeUpdate(BaseModel):
    """Схема для обновления рецепта"""
    admin_approved: bool | None = Field(default=None, description="Одобрен модератором")
    user_approved: bool | None = Field(default=None, description="Одобрен пользователем")


class UserSch(BaseModel):
    id: int
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    is_superuser: Optional[bool] = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    is_deleted: Optional[bool] = False

    class Config:
        from_attributes = True


class RecipesListResponse(BaseModel):
    """Список рецептов с общим количеством для пагинации"""
    items: List[Recipe]
    total: int
