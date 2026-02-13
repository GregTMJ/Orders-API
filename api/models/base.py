"""Модуль содержит базовые модели для формирования таблиц."""

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase, AsyncAttrs):
    __abstract__ = True
