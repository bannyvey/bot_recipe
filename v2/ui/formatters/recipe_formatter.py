from typing import Dict

from pydantic import BaseModel

from v2.schemas.recipe_dto import RecipesPageDTO, RecipeReview
from v2.services.interfaces import IRecipeFormatter
from v2.utils.constants import CATEGORY_MAPPING, CategoryMapping


class RecipePageFormatter(IRecipeFormatter):
    """Форматер для страниц рецептов."""

    def __init__(self):
        self.category_mapping = CATEGORY_MAPPING

    def format_recipe_detail(self, recipe: BaseModel) -> str:
        category_id_to_name = {cat["id"]: cat["name"] for cat in self.category_mapping.values()}
        difficulty_stars = "⭐" * recipe.complexity
        return (
            f"Название блюда: {recipe.title}\n"
            f"Категория рецепта: {category_id_to_name.get(recipe.category_id)}\n"
            f"Описание рецепта: {recipe.description}\n"
            f"Ингредиенты: {recipe.ingredients}\n"
            f"Время готовки в минутах: {recipe.cooking_time}\n"
            f"Сложность: {difficulty_stars}\n"
        )

    @staticmethod
    def format_welcome_message() -> str:
        return """👋 Привет! Я бот для работы с рецептами.

            🍽️ Здесь вы можете:
            • Просматривать все рецепты
            • Просматривать личные рецепты
            • Добавлять новые рецепты
            • Редактировать и удалять рецепты*
            
            Выберите действие в меню ниже:"""

    @staticmethod
    def format_page_header(recipes: RecipesPageDTO) -> str:
        """Отформатировать заголовок страницы с рецептами."""
        if not recipes.items:
            return "Отсутствует список рецептов"
        return f"Текущая страница {recipes.page} из {recipes.pages}.\nВсего рецептов: {recipes.total}"

    @staticmethod
    def format_start_creating_message(username) -> str:
        return (
            f"Привет {username}!)\n\n"
            f"Я бот по самым вкусным рецептам на свете, просто следуй инструкциями и у нас все получится.\n\n"
            f"Просто впиши в наш с тобой чат название рецепта:"
        )

    @staticmethod
    def format_description_prompt() -> str:
        return "Введите описание:"

    @staticmethod
    def format_ingredients_prompt() -> str:
        return "Перечислите ингредиенты:"

    @staticmethod
    def format_cooking_time_prompt() -> str:
        return "Введите время готовки в минутах:"

    @staticmethod
    def format_retry_time_prompt() -> str:
        return "Попробуй еще раз\nНужно ввести просто целое число:"

    @staticmethod
    def format_category_selection_prompt() -> str:
        return "Выбери категорию:"

    @staticmethod
    def format_difficulty_selection_prompt() -> str:
        return "Выберите сложность:"

    @staticmethod
    def get_empty_message() -> str:
        """имитируем сообщение"""
        return "\u2060"
