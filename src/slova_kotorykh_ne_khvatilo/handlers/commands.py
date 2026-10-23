from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from slova_kotorykh_ne_khvatilo.handlers.main_menu.states import MainMenuSG

commands_router = Router()


@commands_router.message(CommandStart())
async def start_handler(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(state=MainMenuSG.main, mode=StartMode.RESET_STACK)
