import logging

from pydantic import BaseModel

from v2.schemas.recipe_dto import RecipesPageDTO, RecipeDTO
from v2.services.interfaces import IAdminService, IApi

logger = logging.getLogger(__name__)


class AdminService(IAdminService):
    def __init__(self, api_client: IApi):
        self.api_client = api_client

    def _dto_model(self, raw_data):
        recipes = [RecipeDTO.model_validate(value) for value in raw_data.get("items", [])]
        return RecipesPageDTO(
            items=recipes,
            total=raw_data.get("total"),
            page=raw_data.get("page"),
            size=raw_data.get("size"),
            pages=raw_data.get("pages")

        )

    @staticmethod
    def _build_recipe_dto(raw_data: dict) -> RecipeDTO:
        return RecipeDTO.model_validate(raw_data)

    async def get_recipe_sent_for_approval(self, page, page_size):
        try:
            recipe_dto = await self.api_client.request(
                "GET",
                "admin/recipes",
                params={"page": page, "limit": page_size}
            )
        except Exception as err:
            logger.error(err)
            raise

        return self._dto_model(recipe_dto)

    async def submit_admin_service(self, recipe_id: int, dto):
        try:
            recipe_dto = await self.api_client.request(
                "PATCH",
                f"admin/{recipe_id}/submit",
                json=dto.model_dump(exclude_none=True)
            )
        except Exception:
            raise

        return self._build_recipe_dto(recipe_dto)
