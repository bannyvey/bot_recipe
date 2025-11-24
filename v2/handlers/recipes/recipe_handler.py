from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from v2.services.interfaces import IRecipeRenderer
from v2.utils.callbacks import RecipeCallback

router = Router()


@router.callback_query(RecipeCallback.filter(F.action == "show_recipes"))
async def show_all_recipes(callback: CallbackQuery, state: FSMContext, recipe_render: IRecipeRenderer):
    """
    Показать все рецепты с пагинацией
    отображает первую страницу с пагинацией

    Args:
        callback: CallbackQuery от пользователя
        state: FSM контекст для хранения состояния
        recipe_render: Рендерер рецептов (инжектируется middleware)
    """

    await recipe_render.show_all_recipes(callback, state, page=1)
