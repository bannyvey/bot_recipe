from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from v2.fms.create_recipe_fms import RecipeStates
from v2.services.interfaces import ICreateRecipeRender, IRecipeFormatter
from v2.utils.callbacks import RecipeCallback


class CreateRecipeRender(ICreateRecipeRender):
    def __init__(
            self,
            user_service,
            recipe_service,
            formatter: IRecipeFormatter,
            keyboard_builder,
            sender,
            recipe_builder
    ):
        self.user_service = user_service
        self.recipe_service = recipe_service
        self.formatter = formatter
        self.keyboard_builder = keyboard_builder
        self.sender = sender
        self.recipe_builder = recipe_builder

    async def start_creating_recipe(self, callback, state):
        username = callback.from_user.username if callback.from_user.username else callback.from_user.first_name
        text = self.formatter.format_start_creating_message(username)
        keyboard = self.keyboard_builder.build_add_recipe_cancel_keyboard()
        message = await self.sender.send_page(callback, text, keyboard)
        await state.set_state(RecipeStates.title)
        await state.update_data(bot_message_id=message.message_id)

    async def title_recipe(self, message, state):
        await message.delete()
        text_title = message.text
        print(text_title)
        text = self.formatter.format_description_prompt()
        await state.update_data(title=text_title)
        data = await state.get_data()
        id_bot_message = data.get("bot_message_id")
        user_chat_id = message.chat.id
        keyboard = self.keyboard_builder.build_add_recipe_cancel_keyboard()
        await state.set_state(RecipeStates.description)
        await self.sender.send_message_fsm(
            message,
            user_chat_id,
            id_bot_message,
            text,
            keyboard
        )


    async def description_recipe(self, message, state):
        await message.delete()
        text_description = message.text
        text = self.formatter.format_ingredients_prompt()
        await state.update_data(description=text_description)
        data = await state.get_data()
        id_bot_massage = data.get("bot_message_id")
        user_chat_id = message.chat.id
        keyboard = self.keyboard_builder.build_add_recipe_cancel_keyboard()
        await state.set_state(RecipeStates.ingredients)
        await self.sender.send_message_fsm(
            message,
            user_chat_id,
            id_bot_massage,
            text,
            keyboard

        )

    async def ingredients_recipe(self, message, state):
        await message.delete()
        text_ingredients = message.text
        await state.update_data(ingredients=text_ingredients)
        text = self.formatter.format_cooking_time_prompt()
        data = await state.get_data()
        id_bot_message = data.get("bot_message_id")
        user_chat_id = message.chat.id
        keyboard = self.keyboard_builder.build_add_recipe_cancel_keyboard()
        await state.set_state(RecipeStates.cooking_time)
        await self.sender.send_message_fsm(
            message,
            user_chat_id,
            id_bot_message,
            text,
            keyboard
        )

    async def time_recipe(self, message, state):
        cooking_time = message.text
        data = await state.get_data()
        id_bot_message = data.get("bot_message_id")
        try:
            cooking_time = int(cooking_time)
            await state.update_data(cooking_time=cooking_time)
            keyboard = self.keyboard_builder.build_category_selection_keyboard()
            text = self.formatter.format_category_selection_prompt()
            await state.set_state(RecipeStates.category_id)
            await self.sender.send_message_fsm(
                message,
                message.chat.id,
                id_bot_message,
                text,
                keyboard
            )
            await message.delete()

        except ValueError:
            await message.delete()
            keyboard = self.keyboard_builder.build_add_recipe_cancel_keyboard()
            text = self.formatter.format_retry_time_prompt()
            try:
                await self.sender.send_message_fsm(
                    message, message.chat.id, id_bot_message, text, keyboard
                )
            except TelegramBadRequest as e:
                if "message is not modified" not in str(e):
                    raise

    async def select_category(self, callback: CallbackQuery, state):
        data = await state.get_data()
        id_bot_message = data.get("bot_message_id")
        chat_id = callback.message.chat.id
        callback_data = RecipeCallback.unpack(callback.data)
        text = self.formatter.format_difficulty_selection_prompt()
        await state.update_data(category=callback_data.name_recipe)
        await state.update_data(category_id=callback_data.recipe_id)
        keyboard = self.keyboard_builder.build_difficulty_selection_keyboard()
        await state.set_state(RecipeStates.difficulty)
        await self.sender.send_callback_fsm(
            callback,
            chat_id,
            id_bot_message,
            text,
            keyboard
        )

    async def select_difficulty(self, callback, state):
        data = await state.get_data()
        id_bot_message = data.get("bot_message_id")
        chat_id = callback.message.chat.id
        callback_data = RecipeCallback.unpack(callback.data)
        await state.update_data(complexity=callback_data.complexity)
        recipe_dto = await self.recipe_builder.build_for_view(state)
        recipe_text = self.formatter.format_recipe_detail(recipe_dto)
        keyboard = self.keyboard_builder.build_confirm_recipe_keyboard()
        await self.sender.send_callback_fsm(
            callback,
            chat_id,
            id_bot_message,
            recipe_text,
            keyboard
        )

    async def save_recipe(self, callback: CallbackQuery, state, telegram_id, is_admin: bool):
        data = await state.get_data()
        id_bot_message = data.get("bot_message_id")
        recipe_dto = await self.recipe_builder.build_for_create(state, telegram_id)
        text = self.formatter.format_welcome_message()
        keyboard = self.keyboard_builder.build_main_menu_keyboard(callback, is_admin)
        await self.recipe_service.create_recipe(recipe_dto)
        await callback.answer("Рецепт успешно создан", show_alert=True)
        await state.clear()
        await self.sender.send_callback_fsm(
            callback,
            callback.message.chat.id,
            id_bot_message,
            text,
            keyboard
        )
