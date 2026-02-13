"""Модуль описание модели валидации работы с пользователями."""

from typing import Annotated
from pydantic import AfterValidator, BaseModel, EmailStr, Field

from helpers.hashers import get_password_hash


class UserRegister(BaseModel):
    email: Annotated[EmailStr, Field(description="Электронная почта пользователя")]
    password: Annotated[
        str, Field(description="Пароль"), AfterValidator(get_password_hash)
    ]


class UserLogin(BaseModel):
    email: Annotated[EmailStr, Field(description="Электронная почта пользователя")]
    password: Annotated[str, Field(description="Пароль")]
