import asyncio

from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from loguru import logger

from slova_kotorykh_ne_khvatilo.db.session import DatabaseSession
from slova_kotorykh_ne_khvatilo.db.utils.ping import ping_database
from slova_kotorykh_ne_khvatilo.handlers import main_router
from slova_kotorykh_ne_khvatilo.middlewares import DBRepositoriesMiddleware
from slova_kotorykh_ne_khvatilo.middlewares.auto_registration import (
    AutoRegistrationMiddleware,
)
from slova_kotorykh_ne_khvatilo.settings import get_settings


async def _main() -> None:
    settings = get_settings()
    if not settings:
        logger.info("Закрываем приложение...")
        return

    database = DatabaseSession(settings.database_url)

    if not await ping_database(database):
        logger.warning("Не удалось подключится БД. Закрываем приложение...")
        return
    logger.success("Подключение к БД доступно.")

    dp = Dispatcher()
    dp.update.outer_middleware.register(DBRepositoriesMiddleware(database.get_session))
    dp.message.middleware.register(AutoRegistrationMiddleware())
    dp.callback_query.middleware.register(AutoRegistrationMiddleware())
    dp.include_router(main_router)
    setup_dialogs(dp)

    bot = Bot(settings.telegram_bot_token)

    await dp.start_polling(bot)


def main() -> None:
    asyncio.run(_main())
