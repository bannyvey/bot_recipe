from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from v2.services.interfaces import IMessageSender


class TelegramMessageSender(IMessageSender):
    """Отправитель сообщений в Telegram."""

    @staticmethod
    async def send_page(event: Message | CallbackQuery, text: str, keyboard: InlineKeyboardMarkup):
        """Отправить страницу с текстом и клавиатурой."""
        if isinstance(event, Message):
            return await event.answer(text, reply_markup=keyboard)
        else:
            return await event.message.edit_text(text, reply_markup=keyboard)


    @staticmethod
    async def send_message_fsm(message: Message, chat_id: int, message_id: int, text: str, keyboard):
        return await message.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=keyboard

        )
    @staticmethod
    async def send_callback_fsm(callback: CallbackQuery, chat_id: int, message_id: int, text: str, keyboard):
        return await callback.message.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=keyboard
        )