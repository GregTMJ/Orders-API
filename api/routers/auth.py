"""Модуль описания взаимодействий с авторизацией и аутентификацией."""

from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, HTTPException, status

from database.connection import get_async_db_session
from database.query import get_user_by_email, authenticate_user
from helpers.auth import create_access_token
from models.users import Users
from redis_core.rate_limiter import RateLimiter
from schemas.users import UserLogin, UserRegister

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="", tags=["Auth"])


@router.post(
    "/register/",
    description="Метод регистрации пользователей.",
    dependencies=[Depends(RateLimiter("5/15s"))],
    responses={
        200: {
            "description": "успешно созданный пользователь",
            "content": {
                "application/json": {
                    "example": {"message": "Пользователь успешно зарегитрирован"}
                }
            },
        },
        400: {
            "description": "Ошибка создания",
            "content": {
                "application/json": {
                    "example": {"detail": "Пользователь уже существует"}
                }
            },
        },
    },
)
async def register(
    user: UserRegister, async_session: "AsyncSession" = Depends(get_async_db_session)
) -> dict:
    check_existing_user = await get_user_by_email(
        email=user.email, async_session=async_session
    )
    if check_existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь уже существует",
        )
    async_session.add(Users(email=user.email, password_hash=user.password))
    await async_session.commit()
    return {"message": "Пользователь успешно зарегитрирован"}


@router.post(
    "/token/",
    description="Метод авторизации пользователей.",
    dependencies=[Depends(RateLimiter("5/1m"))],
    responses={
        200: {
            "description": "Пройдена авторизация",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30"
                    }
                }
            },
        },
        401: {
            "description": "Неверные входные данные",
            "content": {
                "application/json": {"example": {"detail": "Неверная почта или пароль"}}
            },
        },
    },
)
async def get_token(
    user: UserLogin, async_session: "AsyncSession" = Depends(get_async_db_session)
) -> dict:
    user = await authenticate_user(
        email=user.email, password=user.password, async_session=async_session
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверная почта или пароль"
        )
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token}
