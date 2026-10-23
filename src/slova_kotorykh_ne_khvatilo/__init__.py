from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from loguru import logger
from pydantic import ValidationError

from slova_kotorykh_ne_khvatilo.handlers import main_router
from slova_kotorykh_ne_khvatilo.settings import Settings


def get_settings() -> Settings | None:
    try:
        return Settings()  # pyright: ignore[reportCallIssue]
    except ValidationError as ex:
        logger.warning(f"Не удалось получить настройки: {ex}")


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
