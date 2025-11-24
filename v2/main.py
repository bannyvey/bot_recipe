import asyncio
import logging.config
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from logging_config import LOGGING_CONFIG
from v2.handlers import router
from v2.middlewares.container_middleware import ContainerMiddleware
from v2.services.container import container

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('MAIN_BOT')


async def main():
    logger.info("Starting bot")
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.middleware(ContainerMiddleware())
    dp.callback_query.middleware(ContainerMiddleware())
    dp.include_router(router)
    try:
        await dp.start_polling(bot)
    finally:
        await container.shutdown()


if __name__ == '__main__':
    asyncio.run(main())
