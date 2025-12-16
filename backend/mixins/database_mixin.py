from abc import abstractmethod, ABC
from typing import ClassVar, Self, Any, TYPE_CHECKING
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from backend.core.database import Base, ModelAlreadyExistsError, ModelDoesNotExistError
from backend.core.exceptions import ModelNotFoundError, ModelExistsError
from backend.repositories.base import FilterStatementKwargs
from backend.schemas.base import BaseModel

logger = logging.getLogger(__name__)

class _PydanticSanityCheck[Model: BaseModel]:
    _required_methods: ClassVar[tuple[str, ...]] = (
        "model_validate",
        "model_dump_json",
        "model_dump",
    )

    @classmethod
    @abstractmethod
    def model_validate(  # type: ignore[misc]
            cls: type[Model],
            obj: Any,
            *,
            strict: bool | None = None,
            from_attributes: bool | None = None,
            context: dict[str, Any] | None = None,
    ) -> Model: ...


class BaseModelDatabaseMixin[Model: BaseModel](ABC, _PydanticSanityCheck):
    """Миксин для работы с базой данных через Pydantic модели"""

    model: ClassVar[type[Base]]

    id: int

    @classmethod
    async def get(
            cls,
            session: AsyncSession,
            val: int,
            /,
            *,
            field=None,
            extra_where=None
    ) -> Self:
        """Получить объект по ID"""
        try:
            obj: Base = await cls.model.get(session, val)
        except ModelDoesNotExistError as err:
            logger.error(err)
            raise ModelNotFoundError()
        return cls.model_validate(obj)

    @classmethod
    async def paginate(
            cls,
            session: AsyncSession,
            filter_params: FilterStatementKwargs | None = None,
    ) -> Page[Self]:
        """Получить пагинированный список объектов"""
        if filter_params is None:
            filter_params = FilterStatementKwargs(page=0, size=1)
        try:
            statement = cls.model.get_filter_statement(filter_params)
            print(statement)
        except Exception:
            raise
        return await paginate(session, statement)

    @classmethod
    async def create(cls, session: AsyncSession, data: BaseModel) -> Self:
        """Создать новый объект"""
        try:
            obj: Base = await cls.model.create(session, data)
        except ModelAlreadyExistsError as err:
            logger.error(f"Модель уже существует: {err}")
            raise ModelExistsError()
        except Exception as e:
            logger.error(f"ERROR IN MIXIN {e}")
            raise

        return cls.model_validate(obj)

    @classmethod
    async def filter(cls, session: AsyncSession, filter_params: FilterStatementKwargs) -> list[Self]:
        """Получить отфильтрованный список объектов"""
        statement = cls.model.get_filter_statement(filter_params)
        result = await session.execute(statement)
        objects = result.scalars().all()
        return [cls.model_validate(obj) for obj in objects]

    # @classmethod
    # async def count(cls, session: AsyncSession, filter_params: FilterStatementKwargs | None = None) -> int:
    #     """Подсчитать количество объектов"""
    #     if filter_params is None:
    #         filter_params = FilterStatementKwargs()
    #     statement = cls.model.get_filter_statement(filter_params)
    #     count_statement = select(func.count()).select_from(statement.subquery())
    #     result = await session.execute(count_statement)
    #     return result.scalar() or 0

    async def update(self, session: AsyncSession, data: BaseModel | None, **kwargs) -> None:
        """Обновить объект"""
        if data is None and not kwargs:
            raise ValueError("Необходимо передать данные для обновления")
        data_dict = {}
        if data is not None:
            data_dict = data.to_dict()
        obj: Base = await self.model.update(session, self.id, data_dict)
        updated: BaseModel = self.model_validate(obj)
        for field in updated.model_fields_set:
            setattr(self, field, getattr(updated, field))


    async def delete(self, session: AsyncSession) -> None:
        """Удалить объект (мягкое удаление)"""
        await self.model.soft_delete(session, self.id)
