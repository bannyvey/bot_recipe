# from aiogram import Router, F
# from aiogram.exceptions import TelegramBadRequest
# from aiogram.types import CallbackQuery
#
# from bot.utils.constants import HELP_TEXT
# from bot.utils.keyboards.keyboards import get_main_keyboard_for
#
# router = Router()
#
#
# @router.callback_query(F.data == "get_help")
# async def help_handler(callback: CallbackQuery):
#     """Обработчик команды помощи"""
#     try:
#         kb = await get_main_keyboard_for(callback.from_user.id, callback.message.bot)
#         await callback.message.edit_text(
#             HELP_TEXT,
#             reply_markup=kb
#         )
#     except TelegramBadRequest as e:
#         if "message is not modified" in str(e):
#             await callback.answer()
#             pass
#         else:
#             raise e
#     #
