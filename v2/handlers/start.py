import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from v2.filters.is_admin import IsAdmin
from v2.services.interfaces import IUserRender

logger = logging.getLogger(__name__)

start_router = Router()


@start_router.message(Command("start"), IsAdmin())
async def cmd_start(message: Message, is_admin: bool, user_render: IUserRender) -> None:
    """Приветствие и регистрация пользователя."""
    await user_render.user_registration(message, is_admin=is_admin)


@start_router.message(Command("chatid"))
async def chat_id(m: Message):
    """AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"""
    await m.reply(str(m.chat.id))
