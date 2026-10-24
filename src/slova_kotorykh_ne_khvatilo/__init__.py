from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from loguru import logger

from slova_kotorykh_ne_khvatilo.handlers import main_router
from slova_kotorykh_ne_khvatilo.settings import get_settings


def main() -> None:
    settings = get_settings()
    if not settings:
        logger.info("Закрываем приложение...")
        return

    dp = Dispatcher()
    dp.include_router(main_router)
    setup_dialogs(dp)

    bot = Bot(settings.telegram_bot_token)

    dp.run_polling(bot)
