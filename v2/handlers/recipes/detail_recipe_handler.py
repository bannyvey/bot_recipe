from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from v2.filters.is_admin import IsAdmin
from v2.services.interfaces import IRecipeRenderer, IAdminRecipeRender
from v2.utils.callbacks import RecipeCallback

detail_router = Router()


@detail_router.callback_query(RecipeCallback.filter(F.action == "view"))
async def recipe_detail_handler(
        callback: CallbackQuery,
        callback_data: RecipeCallback,
        recipe_render: IRecipeRenderer
):
    """
    Получить рецепт по id

    Args:
        callback: CallbackQuery от пользователя
        callback_data:
        recipe_render: Рендер рецептов(middleware)
    """
    id_recipe = callback_data.recipe_id
    context = callback_data.context
    await recipe_render.show_detail_recipe(callback, id_recipe, context)


@detail_router.callback_query(RecipeCallback.filter(F.action == "back"))
async def back_to_recipes_handler(
        callback: CallbackQuery,
        callback_data: RecipeCallback,
        state: FSMContext,
        recipe_render: IRecipeRenderer,
        admin_render: IAdminRecipeRender
):
    """
    Возврат к списку рецептов с сохранением текущей страницы
    Args:
        callback: CallbackQuery от пользователя
        callback_data: Для получения контекста
        state: FSM для получения текущей страницы
        recipe_render: Рендер рецептов(middleware)
        admin_render: Рендер админ рецептов(middleware)
    """
    context = callback_data.context
    user_id = callback.from_user.id

    if context == "my":
        await recipe_render.show_my_recipes(callback, state, user_id)
    elif context == "all":
        await recipe_render.show_all_recipes(callback, state)
    else:
        await admin_render.render_pending_recipes(callback, state)
