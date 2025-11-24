from functools import cached_property
from typing import Optional

from config import settings
from v2.services.admin_service import AdminService
from v2.services.api_client import APIClient
from v2.services.interfaces import (
    IApi,
    IRecipeService,
    IMessageSender,
    IPageStateManager,
    IRecipeFormatter,
    IRecipeKeyboardBuilder,
    IRecipeRenderer, IUserService, ICreateRecipeRender, IAdminRecipeRender, IAdminService,
    IRecipeBuilder, IUserRender,
)
from v2.services.recipe_builder import RecipeBuilder
from v2.services.recipe_service import RecipeService
from v2.services.user_builder import UserBuilder
from v2.services.user_service import UserService

from v2.ui.components.message_sender import TelegramMessageSender
from v2.ui.components.pagination import PageStateManager
from v2.ui.formatters.recipe_formatter import RecipePageFormatter
from v2.ui.keyboards.recipe_keyboard import RecipeKeyboardsBuilder
from v2.ui.renderers.admin_render import AdminRender
from v2.ui.renderers.create_recipe_render import CreateRecipeRender
from v2.ui.renderers.start_page_render import UserRender
from v2.ui.renderers.recipe_renderer import RecipePageRender


class Container:
    """DI-контейнер с ленивыми свойствами для v2 архитектуры."""

    def __init__(self):
        self._api_client: Optional[APIClient] = None
        self.page_size = settings.page_size

    @cached_property
    def api_client(self) -> IApi:
        """HTTP клиент для работы с backend API."""
        if self._api_client is None:
            self._api_client = APIClient()
        return self._api_client

    @cached_property
    def recipe_builder(self) -> IRecipeBuilder:
        """Билдер для сборки DTO рецептов"""
        return RecipeBuilder()

    @cached_property
    def user_builder(self) -> UserBuilder:
        return UserBuilder()

    @cached_property
    def recipe_service(self) -> IRecipeService:
        """Сервис для работы с рецептами."""
        return RecipeService(self.api_client)

    @cached_property
    def user_service(self) -> IUserService:
        return UserService(self.api_client)

    @cached_property
    def admin_service(self) -> IAdminService:
        return AdminService(self.api_client)

    @cached_property
    def formatter(self) -> IRecipeFormatter:
        """Форматтер для страниц рецептов."""
        return RecipePageFormatter()

    @cached_property
    def keyboard_builder(self) -> IRecipeKeyboardBuilder:
        """Строитель клавиатур для рецептов."""
        return RecipeKeyboardsBuilder()

    @cached_property
    def state_manager(self) -> IPageStateManager:
        """Менеджер состояния пагинации."""
        return PageStateManager()

    @cached_property
    def sender(self) -> IMessageSender:
        """Отправитель сообщений в Telegram."""
        return TelegramMessageSender()

    @cached_property
    def admin_render(self) -> IAdminRecipeRender:
        return AdminRender(
            self.keyboard_builder,
            self.formatter,
            self.admin_service,
            self.sender,
            self.page_size,
            self.state_manager,
            self.recipe_builder
        )

    @cached_property
    def user_render(self) -> IUserRender:
        return UserRender(
            self.user_service,
            self.formatter,
            self.keyboard_builder,
            self.sender,
            self.user_builder,


        )

    @cached_property
    def create_recipe_render(self) -> ICreateRecipeRender:
        return CreateRecipeRender(
            self.user_service,
            self.recipe_service,
            self.formatter,
            self.keyboard_builder,
            self.sender,
            self.recipe_builder
        )

    @cached_property
    def recipe_render(self) -> IRecipeRenderer:
        """Рендерер страниц рецептов."""
        return RecipePageRender(
            self.recipe_service,
            self.user_service,
            self.formatter,
            self.keyboard_builder,
            self.state_manager,
            self.sender,
            self.recipe_builder
        )

    async def shutdown(self) -> None:
        """Закрытие ресурсов (вызвать при завершении работы)."""
        if self._api_client:
            await self._api_client.close()


container = Container()
