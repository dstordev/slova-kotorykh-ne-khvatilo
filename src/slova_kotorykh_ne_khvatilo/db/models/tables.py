from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import BigInteger, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class TelegramUser(Base):
    """Телеграм пользователь."""

    __tablename__ = "telegram_users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    username: Mapped[str | None] = mapped_column(nullable=True, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str | None] = mapped_column(nullable=True)
    is_bot: Mapped[bool]
    language_code: Mapped[str | None] = mapped_column(nullable=True)

    user: Mapped[User | None] = relationship(
        back_populates="telegram_user", lazy="joined"
    )


class User(Base):
    """Пользователь."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int | None] = mapped_column(ForeignKey("telegram_users.id"))
    is_active: Mapped[bool] = mapped_column(server_default=sa.true())
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    telegram_user: Mapped[TelegramUser | None] = relationship(
        back_populates="user", lazy="joined"
    )


class Message(Base):
    """Послание."""

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    from_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
