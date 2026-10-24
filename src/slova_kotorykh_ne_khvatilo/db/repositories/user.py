from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from slova_kotorykh_ne_khvatilo.db.models import TelegramUser, User


class UserRepository:
    """Репозиторий для работы с пользователем."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        telegram_id: int,
        telegram_username: str | None,
        telegram_first_name: str,
        telegram_last_name: str | None,
        telegram_is_bot: bool,
        language_code: str | None,
    ) -> User:
        """Создает пользователя."""

        telegram_user = TelegramUser(
            id=telegram_id,
            username=telegram_username,
            first_name=telegram_first_name,
            last_name=telegram_last_name,
            is_bot=telegram_is_bot,
            language_code=language_code,
        )

        user = User(telegram_id=telegram_id)

        self._session.add(telegram_user)
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)

        return user

    async def find_by_telegram_id(self, telegram_id: int) -> User | None:
        """Ищет пользователя по telegram id."""

        result = await self._session.execute(
            select(User)
            .join(TelegramUser, User.telegram_id == TelegramUser.id)
            .where(TelegramUser.id == telegram_id)
        )

        return result.scalar_one_or_none()
