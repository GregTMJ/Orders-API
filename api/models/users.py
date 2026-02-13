"""Модуль описание модели пользователей."""

from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Users(Base):
    __tablename__ = "users"

    # Columns
    id: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=func.gen_random_uuid()
    )
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]

    def __repr__(self):
        return f"User: {self.id} with email {self.email}"
