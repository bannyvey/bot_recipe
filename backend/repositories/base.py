from typing import NamedTuple, Literal


class FilterStatementKwargs(NamedTuple):
    """Параметры для фильтрации и пагинации"""
    page: int | None = None
    size: int | None = None
    order_by: str | None = "id"
    order_by_direction: Literal["asc", "desc"] = "asc"
    extra: dict | None = None


# class BaseRepository:
#     """Базовый репозиторий для работы с моделями"""
#
#     def __init__(self, model: type[Base]):
#         self.model = model
#
#     async def get(self, session: AsyncSession, val: int) -> Base:
#         """Получить объект по ID"""
#         try:
#             statement = select(self.model).where(self.model.id == val)
#             result = await session.execute(statement)
#             return result.scalar_one()
#         except NoResultFound:
#             raise ModelNotFoundError(f"{self.model.__name__} с ID {val} не найден")
#
#     async def get_or_none(self, session: AsyncSession, val: int) -> Base | None:
#         """Получить объект по ID или None"""
#         try:
#             return await self.get(session, val)
#         except ModelNotFoundError:
#             return None
#
#     def get_filter_statement(self, kwargs: FilterStatementKwargs) -> Select:
#         """Создать SQL запрос с фильтрами"""
#         statement = select(self.model)
#
#         # Сортировка
#         if kwargs.order_by:
#             field = getattr(self.model, kwargs.order_by)
#             if kwargs.order_by_direction == "desc":
#                 statement = statement.order_by(field.desc())
#             else:
#                 statement = statement.order_by(field.asc())
#
#         # Фильтры
#         if kwargs.extra:
#             cond_list = self.get_cond_list(**kwargs.extra)
#             if cond_list:
#                 statement = statement.where(*cond_list)
#
#         # Пагинация
#         if kwargs.offset is not None:
#             statement = statement.offset(kwargs.offset)
#         if kwargs.limit is not None:
#             statement = statement.limit(kwargs.limit)
#
#         return statement
#
#     def get_cond_list(self, **kwargs) -> list:
#         """Получить список условий для фильтрации (переопределяется в наследниках)"""
#         return []
#
#     async def create(self, session: AsyncSession, data: dict) -> Base:
#         """Создать новый объект"""
#         print("----------------------------------")
#         print(data)
#
#         try:
#             obj = self.model(**data)
#             session.add(obj)
#             await session.commit()
#             await session.refresh(obj)
#             return obj
#         except IntegrityError as e:
#             await session.rollback()
#             raise ModelAlreadyExistsError(f"Ошибка создания {self.model.__name__}: {e}")
#
#     async def update(self, session: AsyncSession, id_: int, data: dict) -> Base:
#         """Обновить объект"""
#         obj = await self.get(session, id_)
#
#         for field, value in data.items():
#             if hasattr(obj, field) and value is not None:
#                 setattr(obj, field, value)
#
#         await session.commit()
#         await session.refresh(obj)
#         return obj
#
#     async def soft_delete(self, session: AsyncSession, id_: int) -> None:
#         """Мягкое удаление объекта"""
#         await session.execute(
#             update(self.model)
#             .where(self.model.id == id_)
#             .values(is_deleted=True)
#         )
#         await session.commit()
#
#     async def count(self, session: AsyncSession, filter_params: FilterStatementKwargs | None = None) -> int:
#         """Подсчитать количество объектов"""
#         if filter_params is None:
#             filter_params = FilterStatementKwargs()
#
#         statement = self.get_filter_statement(filter_params)
#         count_statement = select(func.count()).select_from(statement.subquery())
#         result = await session.execute(count_statement)
#         return result.scalar() or 0
