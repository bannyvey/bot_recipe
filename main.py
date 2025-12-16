import asyncio
import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update

from starlette.middleware.cors import CORSMiddleware

from backend.middlewares.swagger_auth import SwaggerAuthMiddleware
from config import settings
from v2.handlers import router as bot_router
from v2.middlewares.container_middleware import ContainerMiddleware
from v2.services.container import container
from backend.main import api_router, add_pagination, run_migrations

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("RUNNER")

bot = Bot(token=settings.bot_token)
dp = Dispatcher(storage=MemoryStorage())
dp.message.middleware(ContainerMiddleware())
dp.callback_query.middleware(ContainerMiddleware())
dp.include_router(bot_router)

WEBHOOK_PATH = "/webhook"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await run_migrations()
    logger.info("Миграции выполнены")

    if settings.webhook_url:
        webhook_url = f"{settings.webhook_url.rstrip('/')}{WEBHOOK_PATH}"
        await bot.set_webhook(url=webhook_url, drop_pending_updates=True)
        logger.info(f"Режим: WEBHOOK → {webhook_url}")
    else:
        logger.info("Режим: POLLING (webhook_url не указан)")

    yield

    await bot.delete_webhook(drop_pending_updates=True)
    await container.shutdown()
    await bot.session.close()
    logger.info("Бот и контейнер выключены")


app = FastAPI(lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.add_middleware(SwaggerAuthMiddleware)

app.include_router(api_router)
add_pagination(app)


@app.post(WEBHOOK_PATH)
async def webhook_handler(request: Request):
    """Обрабатывает обновления от Telegram только в режиме webhook"""
    try:
        update = Update.model_validate(await request.json())
        await dp.feed_update(bot=bot, update=update)
        return JSONResponse({"ok": True})
    except Exception as e:
        logger.error(f"Ошибка обработки webhook: {e}")
        return JSONResponse({"ok": False}, status_code=500)


async def start_polling():
    """Запуск polling в отдельной задаче"""
    logger.info("Запуск polling...")
    await dp.start_polling(bot)


async def main():
    config = uvicorn.Config(
        app,
        host=settings.host,
        port=settings.port,
        log_level="info",
        reload=True
    )
    server = uvicorn.Server(config)

    if settings.webhook_url:
        logger.info("Запуск сервера в режиме WEBHOOK")
        await server.serve()
    else:
        logger.info("Запуск сервера в режиме POLLING + API")
        async with asyncio.TaskGroup() as tg:  # Python 3.11+
            tg.create_task(server.serve())
            tg.create_task(start_polling())


if __name__ == "__main__":
    asyncio.run(main())