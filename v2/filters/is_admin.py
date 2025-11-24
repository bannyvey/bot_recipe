import logging
from typing import Any

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest

from config import settings


logger = logging.getLogger(__name__)


class IsAdmin(Filter):
    """Проверка что пользователь состоит в группе администратора
    """

    async def __call__(self, event: Message | CallbackQuery, *args: Any, **kwargs: Any) -> dict[str, Any]:
        admins_chat_id = getattr(settings, "admins_chat_id", None)
        if not admins_chat_id:
            # If not configured, treat as no admins restriction
            logger.warning("admins_chat_id is not configured; IsAdmin passes by default")
            return {"is_admin": True}

        try:
            bot = event.bot  # both Message and CallbackQuery have .bot
            user_id = (event.from_user.id if event.from_user else None)
            if not user_id:
                return {"is_admin": False}
            member = await bot.get_chat_member(chat_id=int(admins_chat_id), user_id=user_id)
            status = getattr(member, "status", None)
            if status in {"creator", "administrator", "member"}:
                return {"is_admin": True}
            else:
                return {"is_admin": False}

        except TelegramBadRequest as e:
            # e.g. bot is not in the admins chat or cannot access it
            logger.error(f"Failed to check admin membership: {e}")
            return {"is_admin": False}

        except Exception as e:
            logger.exception("Unexpected error in IsAdmin filter: %s", e)
            return {"is_admin": False}


