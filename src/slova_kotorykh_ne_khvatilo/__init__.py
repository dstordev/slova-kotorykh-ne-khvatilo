from aiogram import Bot, Dispatcher
from aiogram.filters.command import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Multi
from loguru import logger
from pydantic import ValidationError

from slova_kotorykh_ne_khvatilo.settings import Settings


def get_settings() -> Settings | None:
    try:
        return Settings()  # pyright: ignore[reportCallIssue]
    except ValidationError as ex:
        logger.warning(f"Не удалось получить настройки: {ex}")


dp = Dispatcher()


class MainSG(StatesGroup):
    main = State()


dialog = Dialog(
    Window(
        Const(
            "😺 Привет!\n"
            "Тут ты можешь получить теплые слова оставленные людьми, а также оставить свои для других"
        ),
        Row(
            Button(Const("📬 Получить"), id="pick_up_message"),
            Button(Const("📥 Оставить"), id="send_message"),
        ),
        state=MainSG.main,
    ),
)


@dp.message(CommandStart())
async def start_handler(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(state=MainSG.main, mode=StartMode.RESET_STACK)


dp.include_router(dialog)

setup_dialogs(dp)


def main() -> None:
    settings = get_settings()
    if not settings:
        logger.info("Закрываем приложение...")
        return

    bot = Bot(settings.telegram_bot_token)

    dp.run_polling(bot)
