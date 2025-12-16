import logging
from typing import Literal

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.params import Depends
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.repositories.base import FilterStatementKwargs
from backend.schemas.recipe_schema import Recipe, RecipeUpdate

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get(
    "/recipes",
    response_model=Page[Recipe],
    status_code=status.HTTP_200_OK
)
async def pending_recipes(
        order_by: str = Query("id", description="Поле для сортировки"),
        direction: Literal["asc", "desc"] = Query("asc", description="Направление сортировки"),
        session: AsyncSession = Depends(get_db)
):
    try:
        filter_par = FilterStatementKwargs(
            order_by=order_by,
            order_by_direction=direction,
            extra={
                "user_approved": True,
                "admin_approved": False
            }
        )
        return await Recipe.paginate(session, filter_par)
    except Exception as err:
        return HTTPException(status_code=500, detail=err)

@router.patch("/{recipe_id}/submit", response_model=Recipe, status_code=status.HTTP_200_OK)
async def approve_recipe(
        recipe_id: int,
        data: RecipeUpdate,
        session: AsyncSession = Depends(get_db)
):
    try:
        recipe = await Recipe.get(session, recipe_id)
        await recipe.update(session, data)
        return recipe
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))


