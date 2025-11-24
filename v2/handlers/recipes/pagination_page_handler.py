from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from v2.services.interfaces import IRecipeRenderer
from v2.utils.callbacks import RecipeCallback


page_router = Router()

@page_router.callback_query(RecipeCallback.filter(F.action == "page"))
async def handle_page_navigation(
        callback: CallbackQuery,
        callback_data: RecipeCallback,
        state: FSMContext,
        recipe_render: IRecipeRenderer
) -> None:
    """
    Обработка навигации по страницам рецептов (все рецепты, личные, для администраторов)

    Args:
        callback: CallbackQuery от пользователя
        callback_data: Данные RecipeCallback для получения сдвига
        state: FSM контекст для хранения состояния
        recipe_render: Рендер рецептов
    """
    context = callback_data.context
    page_num = callback_data.page
    telegram_id = callback.from_user.id
    if context == "my":
        await recipe_render.show_my_recipes(callback, state, telegram_id, page_num)
    else:
        await recipe_render.show_all_recipes(callback, state, page_num)

