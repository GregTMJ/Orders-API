"""Модуль описание модели заказов."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import TIMESTAMP, Enum, Numeric, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from helpers.enums import OrderStatus
from models.base import Base


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=func.gen_random_uuid()
    )
    users_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )
    items: Mapped[list | dict] = mapped_column(JSONB)
    total_price: Mapped[float] = mapped_column(Numeric(precision=12, scale=2))
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), default=OrderStatus.PENDING
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )

    def __repr__(self):
        return f"Order {self.id} has status {self.status}"
