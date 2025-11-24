from typing import Optional, Dict, Any

import aiohttp

from config import settings
from v2.services.interfaces import IApi


class APIClient(IApi):
    def __init__(self):
        self.base_url = settings.backend_url
        self.timeout_second = 15
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        if self.session is None:
            timeout = aiohttp.ClientTimeout(total=self.timeout_second)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session is not None:
            await self.session.close()

    async def request(
            self,
            method: str,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None
    ):
        if self.session is None:
            await self.__aenter__()

        session = self.session
        url = f"{self.base_url}/{endpoint.lstrip("/")}"
        async with session.request(method=method, url=url, params=params, json=json) as resp:
            resp.raise_for_status()
            if resp.content_type == "application/json":
                return await resp.json()
            return await resp.text()

    # async def list_recipes(self, page, limit, user_id: Optional[int] = None):
    #     """Получить рецепты с пагинацией."""
    #     if user_id:
    #         print("ЮЗЕР ЕСТЬ")
    #         return await self._request("GET", f"/recipes/user/{user_id}/", params={"size": limit, "page": page})
    #     else:
    #         # Для всех рецептов
    #         return await self._request("GET", "/recipes/", params={"size": limit, "page": page})
    #
    # async def get_user_by_id(self, telegram_id: int):
    #     return await self._request("GET", f"/users/{telegram_id}/")
    #
    # async def get_recipe(self, recipe_id: int):
    #     return await self._request("GET", f"recipes/{recipe_id}/")
    #
    # async def create_user(self, payload):
    #     return await self._request("POST", "/users/register", json=payload)
    #
    # async def create_recipe(self, payload):
    #     return await self._request("POST", "/recipes/", json=payload)
