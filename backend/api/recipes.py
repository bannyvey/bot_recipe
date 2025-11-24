import logging
from typing import List, Optional, Literal
from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy import select, func, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page

from backend.core.database import get_db, ModelAlreadyExistsError
from backend.core.exceptions import ModelNotFoundError, ModelExistsError
from backend.models.recipe_model import RecipeModel
from backend.models.user_model import UserModel
from backend.schemas.recipe_schema import (
    RecipeCreate, Recipe, RecipeUpdate
)
from backend.repositories.base import FilterStatementKwargs

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("", response_model=Page[Recipe])
async def get_recipes(
        category_id: Optional[int] = Query(None, description="Фильтр по категории"),
        complexity: Optional[int] = Query(None, ge=1, le=5, description="Фильтр по сложности (1-5)"),
        cooking_time_max: Optional[int] = Query(None, ge=1, description="Максимальное время приготовления (минуты)"),
        cooking_time_min: Optional[int] = Query(None, ge=1, description="Минимальное время приготовления (минуты)"),
        search: Optional[str] = Query(None, max_length=100, description="Поиск по названию, описанию или ингредиентам"),
        order_by: str = Query("id", description="Поле для сортировки"),
        direction: Literal["asc", "desc"] = Query("asc", description="Направление сортировки"),
        db: AsyncSession = Depends(get_db)
):
    """Получить список рецептов с фильтрацией и пагинацией. +++ """
    try:
        filter_params = FilterStatementKwargs(
            order_by=order_by,
            order_by_direction=direction,
            extra={
                "admin_approved": True,
            }
        )
        res = await Recipe.paginate(db, filter_params)
        print(res)
        return res
    except Exception as e:
        logging.error(f"Ошибка получения рецептов: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")


@router.get("/{recipe_id}/", response_model=Recipe)
async def get_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    """Получить конкретный рецепт +++"""
    try:
        return await Recipe.get(db, recipe_id)
    except ModelNotFoundError:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    except Exception as e:
        # logger.error(f"Ошибка получения рецепта {recipe_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")


@router.get("/user/{telegram_id}", response_model=Page[Recipe])
async def get_recipes_by_user(
        telegram_id: int,
        order_by: str = Query("id", description="Поле для сортировки"),
        direction: Literal["asc", "desc"] = Query("asc", description="Направление сортировки"),
        db: AsyncSession = Depends(get_db)
):
    """Получить рецепты пользователя с фильтрацией и пагинацией"""
    try:
        filter_params = FilterStatementKwargs(
            order_by=order_by,
            order_by_direction=direction,
            extra={
                "telegram_id": telegram_id,
            }
        )
        obj = await Recipe.paginate(db, filter_params)
        return obj
    except Exception as e:
        logger.error(f"Ошибка получения рецептов пользователя {telegram_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")


@router.post("/", response_model=Recipe)
async def create_recipe(recipe: RecipeCreate, db: AsyncSession = Depends(get_db)):
    """Создать новый рецепт"""
    try:
        return await Recipe.create(db, recipe)
    except ModelExistsError:
        raise HTTPException(
            status_code=422,
            detail="Recipe already exists")
    except Exception as err:
        logger.error(f"ERROR IN CREATE RECIPE {err}")
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(err)}")


@router.patch("/{recipe_id}/submit", response_model=Recipe, status_code=status.HTTP_200_OK)
async def submit_recipe(data: RecipeUpdate, recipe_id: int,  session: AsyncSession = Depends(get_db)):
    """Отправить рецепт на одобрение"""
    try:
        recipe = await Recipe.get(session, recipe_id)
        await recipe.update(session, data)
        return recipe
    except Exception:
        raise HTTPException(status_code=404, detail="Рецепт не найден")


@router.patch("/{recipe_id}", response_model=Recipe)
async def update_recipe(
        recipe_id: int,
        recipe_data: RecipeUpdate,
        db: AsyncSession = Depends(get_db)
):
    """Обновить рецепт"""
    try:
        recipe = await Recipe.get(db, recipe_id)
        await recipe.update(db, recipe_data)
        return recipe
    except ModelNotFoundError:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    # except Exception as e:
    #     # logger.error(f"Ошибка обновления рецепта {recipe_id}: {e}")
    #     raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")


# @router.delete("/{recipe_id}")
# async def delete_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
#     """Удалить рецепт (мягкое удаление)"""
#     try:
#         recipe = await Recipe.get(db, recipe_id)
#         await recipe.delete(db)
#         return {"message": "Рецепт успешно удален"}
#     except ModelNotFoundError:
#         raise HTTPException(status_code=404, detail="Рецепт не найден")
#     except Exception as e:
#         logger.error(f"Ошибка удаления рецепта {recipe_id}: {e}")
#         raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")
