from sqlalchemy import func, select

from slova_kotorykh_ne_khvatilo.db.models import Message, User

from .base import BaseRepository


class MessageRepository(BaseRepository):
    """Репозиторий для работы с посланиями."""

    async def create(self, text: str, from_user: int | User) -> Message:
        """Создает послание."""

        from_user_id = from_user
        if isinstance(from_user, User):
            from_user_id = from_user.id

        message = Message(text=text, from_user=from_user_id)

        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message

    async def get_random_message(self) -> Message | None:
        """Возвращает случайное послание."""

        result = await self._session.execute(
            select(Message).order_by(func.random()).limit(1)
        )
        return result.scalar_one_or_none()
