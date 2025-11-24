import logging
from typing import Optional

from pydantic import BaseModel

from v2.schemas.recipe_dto import RecipesPageDTO, RecipeDTO
from v2.services.interfaces import IApi, IRecipeService

logger = logging.getLogger(__name__)


class RecipeService(IRecipeService):
    """Сервис для работы с рецептами через API."""

    def __init__(self, api_client: IApi):
        self.api_client = api_client

    @staticmethod
    def _build_recipe_dto(raw_data: dict) -> RecipeDTO:
        return RecipeDTO.model_validate(raw_data)

    @staticmethod
    def _build_page_dto(raw_data: dict) -> RecipesPageDTO:
        items = [RecipeDTO.model_validate(item) for item in raw_data.get("items", [])]
        return RecipesPageDTO(
            items=items,
            total=raw_data.get("total", 0),
            page=raw_data.get("page", 1),
            size=raw_data.get("size", 5),
            pages=raw_data.get("pages", 1),
        )

    async def load_all_recipes(self, page, page_size) -> RecipesPageDTO:
        try:
            recipe_data = await self.api_client.request(
                "GET",
                "recipes",
                params={"size": page_size, "page": page}
            )
        except Exception as err:
            logger.error(err)
            raise
        return self._build_page_dto(recipe_data)

    async def load_my_recipes(self, page, page_size, telegram_id: int) -> RecipesPageDTO:
        try:
            recipe_data = await self.api_client.request(
                "GET",
                f"/recipes/user/{telegram_id}",
                params={"size": page_size, "page": page}
            )
        except Exception as err:
            logger.error(err)
            raise
        return self._build_page_dto(recipe_data)

    async def load_recipe(self, recipe_id) -> RecipeDTO:
        try:
            recipe_data = await self.api_client.request("GET", f"recipes/{recipe_id}/")
        except Exception as err:
            logger.error(err)
            raise
        return self._build_recipe_dto(recipe_data)

    async def create_recipe(self, recipe_dto: BaseModel):
        try:
            recipe_data = await self.api_client.request(
                "POST",
                "/recipes/",
                json=recipe_dto.model_dump()
            )
        except Exception as err:
            logger.error(err)
            raise
        return recipe_data

    async def submit_recipe_service(self, recipe_id, update_dto):
        try:
            raw_data = await self.api_client.request(
                "PATCH",
                f"recipes/{recipe_id}/submit",
                json=update_dto.model_dump(exclude_none=True)
            )

        except Exception as err:
            logger.error(f"Ошибка : {err}")
            raise
        return self._build_recipe_dto(raw_data)
