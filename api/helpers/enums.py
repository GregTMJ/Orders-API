"""Модуль описание Enum проекта."""

from enum import Enum

__all__ = ["OrderStatus"]


class OrderStatus(Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    CANCELED = "CANCELED"
