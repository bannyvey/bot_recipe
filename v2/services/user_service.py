import logging

from aiogram.types import Message
from aiohttp import ClientResponseError

from v2.schemas.recipe_dto import UserIdDTO
from v2.schemas.user_dto import UserCreateDTO
from v2.services.interfaces import IApi, IUserService

logger = logging.getLogger(__name__)

class UserService(IUserService):
    def __init__(self, api_client: IApi):
        self.api_client = api_client

    @staticmethod
    def _parse_user_data(message: Message):
        return {
            "telegram_id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name
        }

    @staticmethod
    def _parse_dto(data) -> UserIdDTO:
        return UserIdDTO.model_validate(data)

    async def register_user(self, user_dto):
        try:
            response = await self.api_client.request(
                "POST",
                "users/register",
                json=user_dto.model_dump()
            )
            return response
        except ClientResponseError as err:
            if err.status == 422:
                logger.error(f"Пользователь уже зарегистрирован {err}")
                return None
            else:
                raise


    # async def get_user_by_id(self, telegram_id: int) -> UserIdDTO:
    #     user_data = await self.api_client.request(
    #         "GET",
    #         f"users/{telegram_id}"
    #     )
    #     print(user_data)
    #     return self._parse_dto(user_data)
