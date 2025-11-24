import logging
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from v2.filters.is_admin import IsAdmin
from v2.fms.create_recipe_fms import RecipeStates
from v2.services.interfaces import ICreateRecipeRender
from v2.utils.callbacks import RecipeCallback

create_router = Router()
logger = logging.getLogger(__name__)


@create_router.callback_query(RecipeCallback.filter(F.action == "add_recipe"))
async def create_recipe(callback: CallbackQuery, state: FSMContext, create_recipe_render: ICreateRecipeRender):
    """Активирует FMS создание рецепта"""
    await create_recipe_render.start_creating_recipe(callback, state)


@create_router.message(RecipeStates.title)
async def process_title(message: Message, state: FSMContext, create_recipe_render: ICreateRecipeRender):
    """Название"""
    await create_recipe_render.title_recipe(message, state)


@create_router.message(RecipeStates.description)
async def process_description(message: Message, state: FSMContext, create_recipe_render: ICreateRecipeRender):
    """Описание"""
    await create_recipe_render.description_recipe(message, state)


@create_router.message(RecipeStates.ingredients)
async def process_ingredients(message: Message, state: FSMContext, create_recipe_render: ICreateRecipeRender):
    """Ингридиенты"""
    await create_recipe_render.ingredients_recipe(message, state)


@create_router.message(RecipeStates.cooking_time)
async def process_cooking_time(message: Message, state: FSMContext, create_recipe_render: ICreateRecipeRender):
    """Время готовки"""
    await create_recipe_render.time_recipe(message, state)


@create_router.callback_query(
    RecipeCallback.filter(F.action == "select_category"),
    RecipeStates.category_id
)
async def process_difficulty(callback, state: FSMContext, create_recipe_render: ICreateRecipeRender):
    """Выбор категории"""
    await create_recipe_render.select_category(callback, state)


@create_router.callback_query(
    RecipeCallback.filter(F.action == "select_difficult"),
    RecipeStates.difficulty
)
async def process_difficulty_selection(
        callback: CallbackQuery,
        state: FSMContext,
        create_recipe_render: ICreateRecipeRender
):
    """Выбор сложности"""
    await create_recipe_render.select_difficulty(callback, state)


@create_router.callback_query(
    RecipeCallback.filter(F.action == "confirm_recipe"),
    IsAdmin(),
)
async def process_agree(
        callback: CallbackQuery,
        state: FSMContext,
        is_admin: dict,
        create_recipe_render: ICreateRecipeRender
):
    """Подтверждение рецепта"""
    telegram_user_id = callback.from_user.id
    await create_recipe_render.save_recipe(callback, state, telegram_user_id, is_admin)


@create_router.callback_query(RecipeCallback.filter(F.action == "restart_recipe"))
async def process_cancel(callback: CallbackQuery, state: FSMContext, create_recipe_render: ICreateRecipeRender):
    """Ввести все заново"""
    await create_recipe_render.start_creating_recipe(callback, state)
