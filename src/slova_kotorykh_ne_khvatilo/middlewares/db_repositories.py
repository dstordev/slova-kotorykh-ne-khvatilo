from collections.abc import Awaitable, Callable
from contextlib import AbstractAsyncContextManager
from typing import Any

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from slova_kotorykh_ne_khvatilo.db.repositories.user import UserRepository


class DBRepositoriesMiddleware(BaseMiddleware):
    """Мидлварь для создания сессии и передачи репозиториев в workflow_data."""

    def __init__(
        self, getter_session: Callable[[], AbstractAsyncContextManager[AsyncSession]]
    ) -> None:
        self.getter_session = getter_session

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> None:

        async with self.getter_session() as session:
            data["user_repository"] = UserRepository(session)

            await handler(event, data)
