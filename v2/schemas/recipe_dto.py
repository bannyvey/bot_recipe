from typing import Optional, List

from pydantic import BaseModel, Field


class UserIdDTO(BaseModel):
    id: int


class RecipeReview(BaseModel):
    """Для отображения перед созданием"""
    title: str
    description: str
    ingredients: str
    cooking_time: int
    category_id: int
    complexity: int

class RecipeCreate(BaseModel):
    """Для создания рецепта"""
    title: str
    description: str
    ingredients: str
    cooking_time: int
    category_id: int
    complexity: int
    telegram_id: int

class RecipeUpdate(BaseModel):
    admin_approved: bool | None = Field(default=None, description="Для одобрения от модератора")
    user_approved: bool | None = Field(default=None, description="Для одобрения от пользователя")

class RecipeDTO(BaseModel):
    """Схема одного рецепта"""
    id: int
    title: str
    description: Optional[str] = None
    ingredients: str
    cooking_time: int
    complexity: int
    telegram_id: int
    category_id: int

    class Config:
        from_attributes = True

class RecipesPageDTO(BaseModel):
    """Схема списка рецептов с информацией"""
    items: List["RecipeDTO"]
    total: int
    page: int
    size: int
    pages: int

    class Config:
        from_attributes = True

    @property
    def has_prev(self) -> bool:
        return self.page < 1

    @property
    def has_next(self) -> bool:
        return self.page < self.pages

    @property
    def total_pages(self):
        return self.pages
