"""Модуль описания функции хэширования информации."""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Функция для хэширования пароля.

    Args:
        password (str): Пароль

    Returns:
        str: Хэш пароля.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Функция проверки хэша пароля с переданным хэшом из БД.

    Args:
        plain_password (str): Переданный пароль
        hashed_password (str): Хэш пароля из БД

    Returns:
        bool: True если совпали, иначе False
    """
    return pwd_context.verify(plain_password, hashed_password)
