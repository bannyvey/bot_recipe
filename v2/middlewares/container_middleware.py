from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from v2.services.container import container


class ContainerMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

        data["recipe_render"] = container.recipe_render
        data["create_recipe_render"] = container.create_recipe_render
        data["admin_render"] = container.admin_render
        data["user_render"] = container.user_render


        return await handler(event, data)