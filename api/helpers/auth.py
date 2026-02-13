"""Модуль работы с JWT."""

from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

from fastapi import Depends, HTTPException, Request, status
from jose import jwt, JWTError
from configs import settings
from database.connection import get_async_db_session
from database.query import get_user_by_id

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

__all__ = ["create_access_token", "get_current_user"]


def create_access_token(data: dict) -> str:
    """
    Функция создания токена доступа

    Args:
        data (dict): Данные для зашифровки в токен

    Returns:
        str: Токен по jose.jwt
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_LIFETIME)
    data["exp"] = expire
    encode_jwt = jwt.encode(
        data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encode_jwt


def get_token(request: Request) -> str:
    """
    Функция получения токена из заголовка запроса.

    Args:
        request (Request): Сущность запроса по FastAPI, содержащая информация о запросе.

    Returns:
         str: Токен

    Raises:
        HTTPException: Если не был передан токен
    """
    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        return token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не был передан"
    )


async def get_current_user(
    token: str = Depends(get_token),
    async_session: "AsyncSession" = Depends(get_async_db_session),
):
    """
    Функция обработки переданного токена + аутентификация пользователя.

    Args:
        token (str): Токен
        async_session (AsyncSession): Асинхронная сессия в БД.

    Returns:
        Users: Сущность пользователя

    Raises:
        HTTPException: Ошибку получим если:
            - Токен не найден
            - Токен не валиден
            - Срок давности токен истёк
            - Отсутствует информация по Users.id
            - Пользователь не найден в базе
    """
    error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except JWTError:
        error.detail = "Токен не валиден"
        raise error

    expire = payload.get("exp", 0)
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if not expire or expire_time < datetime.now(timezone.utc):
        error.detail = "Токен истек"
        raise error

    user_id = payload.get("sub")
    if user_id is None:
        error.detail = "Отсутствует идентификатор пользователя"
        raise error

    user = await get_user_by_id(user_id, async_session)
    if user is None:
        error.detail = "Пользователь не найден"
        raise error

    return user
