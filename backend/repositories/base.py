from typing import NamedTuple, Literal


class FilterStatementKwargs(NamedTuple):
    """Параметры для фильтрации и пагинации"""
    page: int | None = None
    size: int | None = None
    order_by: str | None = "id"
    order_by_direction: Literal["asc", "desc"] = "asc"
    extra: dict | None = None
