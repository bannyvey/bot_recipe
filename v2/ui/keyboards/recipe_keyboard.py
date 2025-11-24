from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from v2.schemas.recipe_dto import RecipesPageDTO, RecipeDTO
from v2.services.interfaces import IRecipeKeyboardBuilder
from v2.utils.callbacks import RecipeCallback
from v2.utils.constants import CATEGORY_MAPPING, DIFFICULTY_MAPPING
from v2.utils.enums import RecipeContext


class RecipeKeyboardsBuilder(IRecipeKeyboardBuilder):
    """Строитель клавиатур для рецептов."""

    def __init__(self):
        self.callback = RecipeCallback
        self.category = CATEGORY_MAPPING
        self.complexity = DIFFICULTY_MAPPING

    def _add_back_to_menu_button(self, builder: InlineKeyboardBuilder) -> None:
        builder.button(
            text="🏠 В главное меню",
            callback_data=self.callback(action="main_menu").pack()
        )


    def build_recipes_list_keyboard(self, recipes: RecipesPageDTO,
                                    context: RecipeContext = RecipeContext.ALL
                                    ) -> InlineKeyboardMarkup:

        """Клавиатура для списка рецептов с пагинацией.

        На каждой странице показываем до `page_size` кнопок рецептов и элементы навигации.

        Args:
            recipes: Список рецептов для отображения c текущей страницей, рамером, общим количеством и кол-вом страниц)
            context: Контекст пагинации ("all" для всех рецептов, "my" для моих рецептов, "admin" для одобрения рецептов)
        """
        builder = InlineKeyboardBuilder()

        for recipe in recipes.items:
            title = recipe.title
            recipe_id = recipe.id
            builder.row(InlineKeyboardButton(text=f"🍽 {title}",
                                             callback_data=self.callback(action="view", recipe_id=recipe_id,
                                                                         context=context.value).pack()))
        page = recipes.page
        nav_row: list[InlineKeyboardButton] = []
        if recipes.has_prev:
            nav_row.append(InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=self.callback(action="page", page=page - 1, context=context.value).pack()))
        if recipes.has_next:
            nav_row.append(InlineKeyboardButton(
                text="Вперёд ➡️",
                callback_data=self.callback(action="page", page=page + 1, context=context.value).pack()))
        if nav_row:
            builder.row(*nav_row)
        self._add_back_to_menu_button(builder)
        builder.adjust(1)
        return builder.as_markup()

    def build_recipe_detail_keyboard(self, recipe: RecipeDTO, context) -> InlineKeyboardMarkup:
        """Показывает клавиатуру действий для общих и личных рецептов"""
        builder = InlineKeyboardBuilder()

        builder.button(
            text="⬅️ Назад",
            callback_data=self.callback(action="back", context=context).pack()
        )
        if context == "my":
            builder.button(
                text="📝 Редактировать",
                callback_data=self.callback(action="edit", recipe_id=recipe.id, context=context).pack()
            )
            builder.button(
                text="🗑️ Удалить",
                callback_data=self.callback(action="delete", recipe_id=recipe.id, context=context).pack()
            )
            builder.button(
                text="Отправить на модерацию",
                callback_data=self.callback(action="submit", recipe_id=recipe.id, context=context).pack()
            )
        if context == "admin":
            builder.button(
                text="Одобрить",
                callback_data=self.callback(action="admin_submit", recipe_id=recipe.id, context=context).pack()
            )
        builder.adjust(1)
        return builder.as_markup()

    def build_main_menu_keyboard(self, event: Message, is_admin: bool) -> InlineKeyboardMarkup:
        """Главная клавиатура с условной кнопкой админ-панели для админов."""
        builder = InlineKeyboardBuilder()

        builder.button(text="📖 Все рецепты", callback_data=self.callback(action="show_recipes").pack())
        builder.button(text="🔍 Мои рецепты", callback_data=self.callback(action="my_recipes").pack())
        builder.button(text="➕ Добавить рецепт", callback_data=self.callback(action="add_recipe").pack())
        builder.button(text="❓ Помощь", callback_data=self.callback(action="help").pack())
        if is_admin:
            builder.button(text="🛠 Админ-панель", callback_data=self.callback(action="admin_panel").pack())
        builder.adjust(1)
        return builder.as_markup()

    def build_confirm_recipe_keyboard(self) -> InlineKeyboardMarkup:
        """Клавиатура подтверждения создания рецепта"""
        builder = InlineKeyboardBuilder()

        builder.button(
            text="📝 Подтвердить",
            callback_data=self.callback(action="confirm_recipe").pack(),
        )
        builder.button(
            text="Внести заново",
            callback_data=self.callback(action="restart_recipe"),
        )
        self._add_back_to_menu_button(builder)

        builder.adjust(3)
        return builder.as_markup()

    def build_add_recipe_cancel_keyboard(self) -> InlineKeyboardMarkup:
        """Для возврата в главное меню(если передумал создавать рецепт)"""
        builder = InlineKeyboardBuilder()
        self._add_back_to_menu_button(builder)
        return builder.as_markup()

    def build_category_selection_keyboard(self):
        """Помощник для выбора категории"""
        builder = InlineKeyboardBuilder()
        for callback, name in self.category.items():
            builder.button(text=name["name"],
                           callback_data=self.callback(action="select_category", name_recipe=callback,
                                                       recipe_id=name["id"]).pack())
        self._add_back_to_menu_button(builder)
        builder.adjust(2)
        return builder.as_markup()

    def build_difficulty_selection_keyboard(self):
        """Помощник для выбора сложности"""
        builder = InlineKeyboardBuilder()
        for callback, id_category in self.complexity.items():
            stars = "⭐" * id_category
            builder.button(
                text=stars,
                callback_data=self.callback(action="select_difficult", complexity=id_category).pack()
            )
        builder.adjust(1)
        return builder.as_markup()

    def build_admin_panel_keyboard(self):
        """Кнопки админ панели"""
        builder = InlineKeyboardBuilder()
        builder.button(
            text="Список рецептов на одобрение",
            callback_data=self.callback(action="pending_recipes").pack()
        )
        self._add_back_to_menu_button(builder)
        builder.adjust(1)
        return builder.as_markup()
