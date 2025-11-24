from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from v2.services.interfaces import IAdminRecipeRender
from v2.utils.callbacks import RecipeCallback

admin_router = Router()


@admin_router.callback_query(RecipeCallback.filter(F.action == "admin_panel"))
async def handle_admin_panel_callback(callback: CallbackQuery, admin_render: IAdminRecipeRender):
    """Обработчик callback для открытия админ-панели."""
    await admin_render.render_admin_panel(callback)


@admin_router.callback_query(RecipeCallback.filter(F.action == "pending_recipes"))
async def handle_pending_recipes(callback: CallbackQuery, state: FSMContext, admin_render: IAdminRecipeRender):
    """обработчик одобрения рецептов"""
    await admin_render.render_pending_recipes(callback, state, page=1)

@admin_router.callback_query(RecipeCallback.filter(F.action == "admin_submit"))
async def show_pending_recipes(callback: CallbackQuery,callback_data: RecipeCallback, admin_render: IAdminRecipeRender):

    await admin_render.render_submit_recipe(callback, callback_data)
    # kb = get_recipes_list_keyboard(
    #     recipes=page_data["items"],
    #     page=1,
    #     page_size=PAGE_SIZE,
    #     total=page_data["total"],
    #     context="admin"
    # )
    # text = "Список рецептов (1 страница):"
    #
    # await callback.message.edit_text(text)
    # await callback.message.edit_reply_markup(text, reply_markup=kb)
#
#
# @admin_router.callback_query(F.data.startswith("admin_recipe:"))
# async def get_detail_admin_recipes(callback: CallbackQuery):
#     recipe_id = int(callback.data.split(":")[1])
#
#     recipe_service = await container.recipe_service.get_recipe(recipe_id)
#
#     text = get_text_recipe(recipe_service)
#
#     await callback.message.edit_text(
#         text,
#         reply_markup=get_recipe_keyboard(recipe_id, context="admin")
#     )
#
#
# @admin_router.callback_query(F.data.startswith("approve_recipe:"))
# async def approve_recipe(callback: CallbackQuery):
#     recipe_id = int(callback.data.split(":")[1])
#     user_id = callback.from_user.id
#     await container.admin_service.update_status_moderation(recipe_id)
#
#     await callback.answer(text="Подтвержден", show_alert=True)
#     await callback.message.edit_text(WELCOME_TEXT,
#                                      reply_markup=await get_main_keyboard_for(user_id, callback.message.bot))
