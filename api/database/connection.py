"""Модуль описание подключения к БД."""

from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from helpers.logger import logger
from configs import settings

engine = create_async_engine(
    settings.POSTGRES_URL,
    echo=settings.POSTGRES_ECHO,
    connect_args={
        "server_settings": {
            "statement_timeout": f"{settings.POSTGRES_TRANSACTION_TIMEOUT * 1000}"
        }
    },
)
async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def healthcheck() -> None:
    """Функция статуса подключения к БД."""
    async with async_session_maker() as session:
        try:
            await session.execute(text("SELECT 1"))
            logger.info("Database connected")
        except Exception as e:
            logger.error(f"HealthCheck error: {e}")
            raise e
        finally:
            await session.close()


async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Функция контекстный менеджер создание соединения в БД.
    """
    async with async_session_maker() as async_session:
        try:
            yield async_session
        except Exception as e:
            await async_session.rollback()
            logger.error(f"Transaction error: {e}")
            raise e
        finally:
            await async_session.close()
