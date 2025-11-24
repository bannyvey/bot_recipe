from aiogram import Router, F
from aiogram.types import CallbackQuery

from v2.filters.is_admin import IsAdmin
from v2.services.interfaces import IRecipeRenderer
from v2.utils.callbacks import RecipeCallback

menu = Router()


@menu.callback_query(RecipeCallback.filter(F.action == "main_menu"), IsAdmin())
async def back_to_main_menu(callback: CallbackQuery, is_admin: bool, recipe_render: IRecipeRenderer) -> None:
    """Главное меню"""
    await recipe_render.for_main_menu(callback, is_admin=is_admin)
