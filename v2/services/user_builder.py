from aiogram.types import Message

from v2.schemas.user_dto import UserCreateDTO


class UserBuilder:
    """Отвечает только за сборку DTO из Message."""

    @staticmethod
    def build_from_message(message: Message) -> UserCreateDTO:
        """Создает UserCreateDTO из Telegram Message."""
        return UserCreateDTO(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )

