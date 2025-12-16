import base64
import os
import secrets

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED

from config import settings

# Пути, которые нужно защищать
PROTECTED_PATHS = {"/docs", "/redoc", "/openapi.json"}  # можно добавить другие


class SwaggerAuthMiddleware(BaseHTTPMiddleware):
    """Защищает Swagger UI и OpenAPI JSON с помощью Basic Auth из .env"""

    def __init__(self, app):
        super().__init__(app)
        # Обязательно берём из .env — никаких значений по умолчанию!
        self.username = getattr(settings, "swagger_user", None)
        self.password = getattr(settings, "swagger_password", None)

        if not self.username or not self.password:
            raise ValueError(
                "Для защиты Swagger обязательно укажите SWAGGER_USER и SWAGGER_PASSWORD в .env файле"
            )

    async def dispatch(self, request: Request, call_next):
        # Проверяем, попадает ли путь под защиту
        if request.url.path in PROTECTED_PATHS or request.url.path.startswith("/docs/"):
            auth = request.headers.get("Authorization")

            if not auth or not auth.startswith("Basic "):
                return self._unauthorized()

            try:
                # Декодируем "login:password"
                encoded = auth.split(" ", 1)[1]
                decoded = base64.b64decode(encoded).decode("utf-8")
                user, _, pwd = decoded.partition(":")
            except Exception:
                return self._unauthorized()

            # Безопасное сравнение (защита от timing attack)
            if not (
                secrets.compare_digest(user, self.username)
                and secrets.compare_digest(pwd, self.password)
            ):
                return self._unauthorized()

        # Если путь не защищённый или авторизация прошла — пропускаем дальше
        return await call_next(request)

    @staticmethod
    def _unauthorized() -> Response:
        return Response(
            content="Unauthorized",
            status_code=HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": 'Basic realm="Swagger UI"'},
        )