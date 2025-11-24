from aiogram.filters.callback_data import CallbackData


class RecipeCallback(CallbackData, prefix="recipe"):
    action: str
    page: int | None = None
    recipe_id: int | None = None
    name_recipe: str | None = None
    complexity: int | None = None
    context: str | None = None


# callback_data_for_menu = RecipeCallback(action="back_menu", page=None, recipe_id=None, context=None)
