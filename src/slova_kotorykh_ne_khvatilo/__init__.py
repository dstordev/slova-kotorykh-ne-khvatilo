from aiogram import Bot, Dispatcher
from aiogram.filters.command import CommandStart
from aiogram.types import Message
from loguru import logger
from pydantic import ValidationError

from slova_kotorykh_ne_khvatilo.settings import Settings


def get_settings() -> Settings | None:
    try:
        return Settings()  # pyright: ignore[reportCallIssue]
    except ValidationError as ex:
        logger.warning(f"Не удалось получить настройки: {ex}")


dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.reply("Hi")


def main() -> None:
    settings = get_settings()
    if not settings:
        logger.info("Закрываем приложение...")
        return

    bot = Bot(settings.telegram_bot_token)

    dp.run_polling(bot)
