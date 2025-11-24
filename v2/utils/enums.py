from enum import Enum


class RecipeContext(str, Enum):
    """Enum для контекстов пагинации"""
    ALL = "all"
    MY = "my"
    ADMIN = "admin"
