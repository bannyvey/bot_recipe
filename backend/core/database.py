from datetime import datetime
from typing import Optional, Self

import logging

import asyncpg
from asyncpg import UniqueViolationError, ForeignKeyViolationError
from sqlalchemy import Integer, MetaData, func, select
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import as_declarative, mapped_column, Mapped
from sqlalchemy.orm import DeclarativeBaseNoMeta as _DeclarativeBase

from backend.schemas.base import BaseModel

# logger = logging.getLogger(__name__)

BASE_URL = "postgresql+asyncpg://postgres:callofduty@localhost:5432/recipe_bot"


class ModelBaseError(Exception): ...


class ModelAlreadyExistsError(ModelBaseError): ...


class ModelDoesNotExistError(ModelBaseError): ...


class ModelForeignKeyViolationError(ModelBaseError): ...


class DeclarativeBaseNoMeta(_DeclarativeBase):
    pass


@as_declarative()
class Base:
    metadata = MetaData
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )
    is_deleted: Mapped[Optional[bool]] = mapped_column(default=False)

    @classmethod
    async def get(
            cls,
            session,
            val,
            /,
            *,
            field=None,
            extra_where=None
    ) -> Self:
        if field is None:
            field = cls.id
        where_cond: list = [field == val]
        if extra_where is not None:
            where_cond.extend(extra_where)

        cursor = await session.scalars(select(cls).where(*where_cond))
        try:
            return cursor.first()
        except NoResultFound:
            raise

    @classmethod
    async def create(
            cls,
            session: AsyncSession,
            data: BaseModel,
    ) -> Self:
        obj: Self = cls(**data.to_dict())  # type: ignore
        session.add(obj)
        try:
            await session.commit()
        except IntegrityError as err:
            await session.rollback()
            if err.orig.sqlstate == UniqueViolationError.sqlstate:
                raise ModelAlreadyExistsError()
            raise
        return obj

    @classmethod
    async def update(cls, session: AsyncSession, id_: int, data, /, ) -> Self:
        try:
            obj: Self = await cls.get(session, id_)
        except ModelDoesNotExistError:
            raise
        for field, value in data.items():
            setattr(obj, field, value)
        await session.commit()
        return obj

    @classmethod
    async def soft_delete(cls, session, id_):
        obj = await cls.get(session, id_, field=None, extra_where=None)
        obj.is_deleted = True
        await session.commit()

    @classmethod
    def get_filter_statement(cls, kwargs) -> "Select":
        """Создать SQL запрос с фильтрами (базовая реализация)"""
        from sqlalchemy import select
        statement = select(cls)

        # Сортировка
        if kwargs.order_by:
            field = getattr(cls, kwargs.order_by)
            if kwargs.order_by_direction == "desc":
                statement = statement.order_by(field.desc())
            else:
                statement = statement.order_by(field.asc())

        # Фильтры
        if kwargs.extra:
            cond_list = cls.get_cond_list(**kwargs.extra)
            if cond_list:
                statement = statement.where(*cond_list)

        # Пагинация
        if kwargs.page is not None:
            statement = statement.offset(kwargs.page)
        if kwargs.size is not None:
            statement = statement.limit(kwargs.size)

        return statement

    # @classmethod
    # def get_cond_list(cls, **kwargs) -> list:
    #     print("AAAAAAAAAAAa")
    #     """Получить список условий для фильтрации (переопределяется в наследниках)"""
    #     for field, value in kwargs.items():
    #         field=value
    #
    #         print(field)
    #     return []


# Асинхронный движок для Alembic
engine = create_async_engine(
    BASE_URL,
    echo=False
)

async_local_session = async_sessionmaker(
    bind=engine, expire_on_commit=False,
)


async def get_db():
    async with async_local_session() as session:
        yield session
