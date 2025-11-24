from typing import Optional

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from v2.services.interfaces import (
    IRecipeService,
    IMessageSender,
    IPageStateManager,
    IRecipeFormatter,
    IRecipeKeyboardBuilder,
    IRecipeRenderer, IUserService, IRecipeBuilder
)
from v2.utils.enums import RecipeContext


class RecipePageRender(IRecipeRenderer):
    """Рендер страниц рецептов."""

    def __init__(
            self,
            recipe_service: IRecipeService,
            user_service: IUserService,
            formatter: IRecipeFormatter,
            keyboard_builder: IRecipeKeyboardBuilder,
            state_manager: IPageStateManager,
            sender: IMessageSender,
            recipe_builder: IRecipeBuilder,
            page_size: int = 5
    ):
        self.recipe_service = recipe_service
        self.user_service = user_service
        self.formatter = formatter
        self.keyboard_builder = keyboard_builder
        self.state_manager = state_manager
        self.sender = sender
        self.recipe_builder = recipe_builder
        self.page_size = page_size

    async def show_all_recipes(self, callback: CallbackQuery, state: FSMContext, page: Optional[int] = None):
        """Рендер для всех рецептов с пагинацией"""
        if page is None:
            page = await self.state_manager.get_page(state, "current_page")
        await self.state_manager.save_page(state, "current_page", page)
        recipe_data = await self.recipe_service.load_all_recipes(page, self.page_size)
        text = self.formatter.format_page_header(recipe_data)  # вопрос про async
        keyboard = self.keyboard_builder.build_recipes_list_keyboard(recipe_data, RecipeContext.ALL)
        await self.sender.send_page(callback, text, keyboard)

    async def show_my_recipes(self, callback: CallbackQuery, state: FSMContext, telegram_id,
                              page: Optional[int] = None):
        if page is None:
            page = await self.state_manager.get_page(state, "my_current_page")
        await self.state_manager.save_page(state, "my_current_page", page)
        recipe_data = await self.recipe_service.load_my_recipes(page, self.page_size, telegram_id)
        text = self.formatter.format_page_header(recipe_data)
        keyboard = self.keyboard_builder.build_recipes_list_keyboard(recipe_data, RecipeContext.MY)
        await self.sender.send_page(callback, text, keyboard)

    async def show_detail_recipe(self, callback, recipe_id, context):
        recipe_data = await self.recipe_service.load_recipe(recipe_id)
        text = self.formatter.format_recipe_detail(recipe_data)
        keyboard = self.keyboard_builder.build_recipe_detail_keyboard(recipe_data, context)
        await self.sender.send_page(callback, text, keyboard)


    async def for_main_menu(self, callback, is_admin):
        keyboard = self.keyboard_builder.build_main_menu_keyboard(callback, is_admin)
        text = self.formatter.format_welcome_message()
        await self.sender.send_page(callback, text, keyboard)

    async def render_submit_recipe(self, callback: CallbackQuery, state, callback_data):
        recipe_id = callback_data.recipe_id
        recipe_update_dto = await self.recipe_builder.build_for_update_status(user_approved=True)
        print(recipe_update_dto)
        await self.recipe_service.submit_recipe_service(recipe_id, recipe_update_dto)
        await callback.answer(
            "Рецепт отправлен на одобрение",
            show_alert=True
        )