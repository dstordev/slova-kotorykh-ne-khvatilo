from aiogram import Router

from .commands import commands_router
from .main_menu import dialog

main_router = Router()

main_router.include_routers(
    commands_router,
    dialog,
)

__all__ = ["main_router"]
