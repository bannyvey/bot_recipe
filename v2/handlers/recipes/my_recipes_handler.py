from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


from v2.services.interfaces import IRecipeRenderer
from v2.utils.callbacks import RecipeCallback

my_recipes_router = Router()


@my_recipes_router.callback_query(RecipeCallback.filter(F.action == "my_recipes"))
async def get_my_recipes(callback: CallbackQuery, state: FSMContext, recipe_render: IRecipeRenderer):
    """
    Получить список рецептов текущего юзера
    Args:
        callback: Callback от пользователя
        state: обновить текущую страницу
        recipe_render: Рендер рецептов(middleware)
    """
    telegram_id = callback.from_user.id
    await recipe_render.show_my_recipes(callback, state, telegram_id, page=1)


@my_recipes_router.callback_query(RecipeCallback.filter(F.action == "submit"))
async def submit_recipe(
        callback: CallbackQuery,
        state: FSMContext,
        callback_data: RecipeCallback,
        recipe_render: IRecipeRenderer
):
    await recipe_render.render_submit_recipe(callback, state, callback_data)


# @my_recipes_router.callback_query(F.data.startswith("submit_recipe:"))
# async def send_to_moderation(callback: CallbackQuery):
#     try:
#         recipe_id = int(callback.data.split(":")[1])
#         recipe_service = await container.recipe_service.send_recipe_to_moderation(recipe_id)
#         await callback.answer(text="Отправлено на проверку", show_alert=True)
#     except:
#         await callback.answer(text="Уже отправлено на проверку", show_alert=True)
