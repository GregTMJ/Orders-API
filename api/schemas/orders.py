"""модуль валидации данных по заказам."""

from datetime import datetime
from decimal import Decimal
from typing import Annotated, Any
from uuid import UUID
from pydantic import BaseModel, Field, TypeAdapter

from helpers.enums import OrderStatus


class OrderCreate(BaseModel):
    items: Annotated[list[Any], Field(description="Список товаров")]
    total_price: Annotated[
        Decimal,
        Field(gt=0.01, description="Цена", decimal_places=2, examples=[1000.00]),
    ]
    status: Annotated[OrderStatus, Field(description="Статус заказа")]


class Order(BaseModel):
    id: Annotated[UUID, Field(description="Уникальный идентификато")]
    items: Annotated[list[Any], Field(description="Список товаров")]
    total_price: Annotated[
        Decimal, Field(description="Цена", decimal_places=2, examples=[1000.00])
    ]
    status: Annotated[OrderStatus, Field(description="Статус заказа")]
    created_at: Annotated[datetime, Field(description="Дата-время создания заказа")]

    class Config:
        from_attributes = True


class OrderUpdate(BaseModel):
    status: Annotated[OrderStatus, Field(description="Изменение статуса.")]


Orders = TypeAdapter(list[Order])
