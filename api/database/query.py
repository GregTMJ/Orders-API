"""Модуль работы с БД."""

from typing import TYPE_CHECKING
from sqlalchemy import select

from helpers.hashers import verify_password
from models.orders import Orders
from models.users import Users

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_by_email(email: str, async_session: "AsyncSession") -> Users | None:
    """
    Функция для получения данных пользователя по почте.

    Args:
        email (str): Почта
        async_session (AsyncSession): Асинхронная сессия в БД.

    Returns:
         Users | None: Информация по пользователю, если найдена
    """
    user_exists = select(Users).where(Users.email == email)
    return await async_session.scalar(user_exists)


async def get_user_by_id(id_: str, async_session: "AsyncSession") -> Users | None:
    """
    Функция для получения данных пользователя по идентификатору.

    Args:
        id_ (str): Идентификатор
        async_session (AsyncSession): Асинхронная сессия в БД.

    Returns:
        Users | None: Информация по пользователю, если найдена
    """
    user = select(Users).where(Users.id == id_)
    return await async_session.scalar(user)


async def authenticate_user(
    email: str, password: str, async_session: "AsyncSession"
) -> Users | None:
    """
    Функция проверки пользователя по почте и пароли.

    Args:
        email (str): Почта
        password (str): Пароль
        async_session (AsyncSession): Асинхронная сессия в БД.

    Returns:
        Users | None: Информация по пользователю, если найдена
    """
    stmt = select(Users).where(Users.email == email)
    user: Users | None = await async_session.scalar(stmt)
    if user is None:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


async def get_order_by_id(id_: str, async_session: "AsyncSession") -> Orders | None:
    """
    Функция для получения данных заказа по идентификатору.

    Args:
        id_ (str): Идентификатор
        async_session (AsyncSession): Асинхронная сессия в БД.

    Returns:
        Orders | None: Информация по заказу, если найдена
    """
    stmt = select(Orders).where(Orders.id == id_)
    return await async_session.scalar(stmt)


async def get_orders(
    async_session: "AsyncSession",
    user_id: str | None = None,
) -> list[Orders] | list:
    """
    Функция для получения данных заказов.
    В случае передачи идентификатора пользователя -> выдаются заказы пользователя.

    Args:
        user_id (str): Идентификатор
        async_session (AsyncSession): Асинхронная сессия в БД.

    Returns:
        list[Orders] | list: Информация по заказам, если найдены иначе пустой список
    """
    stmt = select(Orders)
    if user_id is not None:
        stmt = stmt.where(Orders.users_id == user_id)
    return await async_session.scalars(stmt)
