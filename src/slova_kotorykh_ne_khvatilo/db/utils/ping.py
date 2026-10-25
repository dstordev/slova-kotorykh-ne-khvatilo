import sqlalchemy as sa
from loguru import logger

from slova_kotorykh_ne_khvatilo.db.session import Database


async def ping_database(database: Database) -> bool:
    """Пингует БД."""

    async with database.get_session() as session:
        try:
            await session.execute(sa.text("SELECT 1"))
            return True
        except OSError as ex:
            if "Connect call failed" in str(ex):
                logger.error(
                    "[ping_database] Ошибка подключения, проверьте включена ли БД."
                )
            else:
                logger.error(f"[ping_database] Неизвестная системная ошибка: {ex}")
        except Exception as ex:
            logger.error(f"[ping_database] Неизвестная ошибка: {ex}")
        return False
