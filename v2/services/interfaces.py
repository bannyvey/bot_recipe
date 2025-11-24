from __future__ import annotations
from typing import Protocol, Optional, Dict, Any, TYPE_CHECKING
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.fsm.context import FSMContext

if TYPE_CHECKING:
    from v2.schemas.recipe_dto import RecipesPageDTO, RecipeDTO


class IApi(Protocol):
    """Интерфейс для работы с API рецептов."""

    async def request(self,
                      method: str,
                      endpoint: str,
                      params: Optional[Dict[str, Any]] = None,
                      json: Optional[Dict[str, Any]] = None): ...

    async def list_recipes(self, page: int, limit: int, user_id: Optional[int] = None) -> Dict[str, Any]: ...

    async def get_user_by_id(self, telegram_id: int) -> Dict[str, Any]: ...

    async def get_recipe(self, recipe_id): ...

    async def create_user(self, message): ...

    async def close(self) -> None: ...

    async def admin_render(self) -> None: ...


class IUserRender(Protocol):
    async def user_registration(self, message: Message, is_admin: bool): ...


class ICreateRecipeRender(Protocol):
    async def start_creating_recipe(self, callback, state): ...

    async def title_recipe(self, message, state): ...

    async def description_recipe(self, message, state): ...

    async def ingredients_recipe(self, message, state): ...

    async def time_recipe(self, message, state): ...

    async def select_category(self, callback, state): ...

    async def select_difficulty(self, callback, state): ...

    async def save_recipe(self, callback, state, telegram_user_id, is_admin): ...


class IUserRegistrationService(Protocol):
    async def register_user(self): ...


class IRecipeService(Protocol):
    """Интерфейс сервиса для работы с рецептами."""

    async def load_all_recipes(self, page: int, page_size: int) -> RecipesPageDTO: ...

    async def load_my_recipes(self, page, page_size, user_id) -> RecipesPageDTO: ...

    async def load_recipe(self, recipe_id) -> RecipeDTO: ...

    async def submit_recipe_service(self, recipe_id, recipe_dto): ...


class IUserService(Protocol):
    """Интерфейс сервиса для работы с пользователями"""

    async def get_user_by_id(self, telegram_id: int) -> "UserIdDTO": ...

    async def register_user(self, message): ...


class IMessageSender(Protocol):
    """Интерфейс для отправки сообщений в Telegram."""

    @staticmethod
    async def send_page(event: Message | CallbackQuery, text: str, keyboard: InlineKeyboardMarkup) -> None: ...

    @staticmethod
    async def send_callback_fsm(callback: CallbackQuery, chat_id: int, message_id: int, text: str, keyboard): ...


class IPageStateManager(Protocol):
    """Интерфейс для управления состоянием пагинации."""

    @staticmethod
    async def get_page(state: FSMContext, key: str, default: int = 1) -> int: ...

    @staticmethod
    async def save_page(state: FSMContext, key: str, page: int) -> None: ...


class IRecipeFormatter(Protocol):
    """Интерфейс для форматирования страниц рецептов."""

    @staticmethod
    def format_page_header(recipes: "RecipesPageDTO") -> str: ...

    def format_recipe_detail(self, recipe: "RecipeDTO"): ...

    @staticmethod
    def format_welcome_message(): ...

    @staticmethod
    def get_empty_message(): ...

    @staticmethod
    def format_start_creating_message(username): ...

    @staticmethod
    def format_description_prompt() -> str: ...

    @staticmethod
    def format_ingredients_prompt(): ...

    @staticmethod
    def format_cooking_time_prompt(): ...

    @staticmethod
    def format_category_selection_prompt(): ...

    @staticmethod
    def format_retry_time_prompt(): ...

    @staticmethod
    def format_difficulty_selection_prompt(): ...


class IRecipeKeyboardBuilder(Protocol):
    """Интерфейс для создания клавиатур рецептов."""

    @staticmethod
    def build_recipes_list_keyboard(recipes: "RecipesPageDTO",
                                    context: "RecipeContext" = "RecipeContext.ALL") -> InlineKeyboardMarkup: ...

    @staticmethod
    def build_recipe_detail_keyboard(recipe, context) -> InlineKeyboardMarkup: ...

    @staticmethod
    def build_main_menu_keyboard(event, is_admin: bool) -> InlineKeyboardMarkup: ...


class IRecipeRenderer(Protocol):
    """Интерфейс для рендеринга страниц рецептов."""

    async def show_all_recipes(self, callback: CallbackQuery, state: FSMContext,
                               page: Optional[int] = None) -> None: ...

    async def show_my_recipes(self, callback: CallbackQuery, state: FSMContext, telegram_id: int,
                              page: Optional[int] = 1) -> None: ...

    async def show_detail_recipe(self, callback, recipe_id, context):  ...

    async def render_submit_recipe(self, callback, state, callback_data): ...

    async def for_main_menu(self, callback, is_admin): ...


class IAdminRecipeRender(Protocol):
    async def render_admin_panel(self, callback): ...

    async def render_pending_recipes(self, callback, state, page: int | None = None): ...

    async def render_submit_recipe(self, callback, callback_data): ...


class IAdminService(Protocol):
    async def get_recipe_sent_for_approval(self, page, page_size): ...


class IRecipeBuilder(Protocol):
    async def build_for_update_status(self, admin_approved: bool | None = None, user_approved: bool | None = None): ...
