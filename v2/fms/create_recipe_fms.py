from aiogram.fsm.state import StatesGroup, State


class RecipeStates(StatesGroup):
    """Состояния для создания рецепта"""
    title = State()
    description = State()
    ingredients = State()
    cooking_time = State()
    category_id = State()
    difficulty = State()
