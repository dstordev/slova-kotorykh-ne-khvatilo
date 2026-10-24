from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import (
    CallbackQuery,
    ChatJoinRequest,
    ChatMemberUpdated,
    ChosenInlineResult,
    InlineQuery,
    Message,
    PaidMediaPurchased,
    PreCheckoutQuery,
    ShippingQuery,
    TelegramObject,
)

from slova_kotorykh_ne_khvatilo.db.repositories.user import UserRepository

ALLOW_EVENTS = (
    Message,
    CallbackQuery,
    ChatJoinRequest,
    ChatMemberUpdated,
    InlineQuery,
    ChosenInlineResult,
    ShippingQuery,
    PreCheckoutQuery,
    PaidMediaPurchased,
)


class AutoRegistrationMiddleware(BaseMiddleware):
    """
    Мидлварь для автоматической регистрации, срабатывающий на некоторые события пользователя.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> None:
        if isinstance(event, ALLOW_EVENTS) and (telegram_user := event.from_user):
            user_repository: UserRepository = data["user_repository"]
            if not await user_repository.find_by_telegram_id(telegram_user.id):
                await user_repository.create(
                    telegram_user.id,
                    telegram_user.username,
                    telegram_user.first_name,
                    telegram_user.last_name,
                    telegram_user.is_bot,
                    telegram_user.language_code,
                )

        await handler(event, data)
