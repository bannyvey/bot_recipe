from aiogram.types import CallbackQuery
from pydantic import BaseModel

from v2.services.interfaces import IAdminRecipeRender, IMessageSender, IRecipeKeyboardBuilder, IRecipeFormatter, \
    IPageStateManager, IAdminService
from v2.utils.enums import RecipeContext


class AdminRender(IAdminRecipeRender):
    def __init__(
            self,
            keyboard_builder: IRecipeKeyboardBuilder,
            formatter: IRecipeFormatter,
            admin_service: IAdminService,
            sender: IMessageSender,
            page_size,
            state_manager: IPageStateManager,
            recipe_builder
    ):
        self.keyboard_builder = keyboard_builder
        self.formatter = formatter
        self.admin_service = admin_service
        self.sender = sender
        self.page_size = page_size
        self.state_manager = state_manager
        self.recipe_builder = recipe_builder

    async def render_admin_panel(self, callback):
        keyboard = self.keyboard_builder.build_admin_panel_keyboard()
        text = self.formatter.get_empty_message()
        await self.sender.send_page(
            callback,
            text,
            keyboard
        )

    async def render_pending_recipes(self, callback, state, page: int | None = None):
        if page is None:
            page = await self.state_manager.get_page(state, "admin_page")
        await self.state_manager.save_page(state, "admin_page", page)
        recipe_dto = await self.admin_service.get_recipe_sent_for_approval(page, self.page_size)
        keyboard = self.keyboard_builder.build_recipes_list_keyboard(recipe_dto, RecipeContext.ADMIN)
        await self.sender.send_page(
            callback,
            self.formatter.get_empty_message(),
            keyboard
        )

    async def render_submit_recipe(self, callback: CallbackQuery, callback_data):
        recipe_id = callback_data.recipe_id
        print(recipe_id)
        recipe_dto: BaseModel = await self.recipe_builder.build_for_update_status(admin_approved=True)
        await self.admin_service.submit_admin_service(recipe_id, recipe_dto)
        await callback.answer(
            "Рецепт одобрен",
            show_alert=True
        )