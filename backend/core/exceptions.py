"""Кастомные исключения для приложения"""


class BaseAppException(Exception):
    """Базовое исключение приложения"""
    ...

class ModelExistsError(Exception): ...

class ModelNotFoundError(Exception): ...
