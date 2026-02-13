"""Модуль описание работы с заказами."""

import json
from typing import TYPE_CHECKING
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer

from configs import settings
from database.connection import get_async_db_session
from database.query import get_order_by_id, get_orders
from helpers.auth import get_current_user
from models.orders import Orders as SqlOrders
from rabbit_core.client import rmq_client
from redis_core.client import redis_client
from schemas.orders import Order, OrderCreate, OrderUpdate

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from models.users import Users


security = HTTPBearer()

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post(
    "/",
    description="Создание нового заказа",
    responses={
        201: {
            "description": "Успешное создание",
            "model": Order,
        },
        401: {
            "description": "Ошибки авторизации",
            "content": {
                "application/json": {"example": {"detail": "Токен не валиден"}}
            },
        },
    },
)
async def create_order(
    order: OrderCreate,
    _auth=Depends(security),
    async_session: "AsyncSession" = Depends(get_async_db_session),
    current_user: "Users" = Depends(get_current_user),
) -> Order:
    new_order = SqlOrders(
        users_id=current_user.id,
        **order.model_dump(),
    )
    async_session.add(new_order)
    await async_session.commit()
    await async_session.flush([new_order])

    await rmq_client.send_message(
        exchange_name=settings.RMQ_EXCHANGE,
        queue_name=settings.RMQ_QUEUE,
        message=json.dumps({"order_id": str(new_order.id)}),
        task_name="new_order",
    )

    return new_order


@router.get(
    "/",
    description="Получить все заказы",
    responses={
        200: {
            "description": "Заказы",
            "model": list[Order],
        },
        401: {
            "description": "Ошибки авторизации",
            "content": {
                "application/json": {"example": {"detail": "Токен не валиден"}}
            },
        },
    },
)
async def get_all_orders(
    _auth=Depends(security),
    async_session: "AsyncSession" = Depends(get_async_db_session),
    _: "Users" = Depends(get_current_user),
) -> list[Order]:
    return await get_orders(async_session)


@router.get(
    "/{order_id}/",
    description="Получить данные по заказу",
    responses={
        200: {
            "description": "Данные по конкретному заказу",
            "model": Order,
        },
        401: {
            "description": "Ошибки авторизации",
            "content": {
                "application/json": {"example": {"detail": "Токен не валиден"}}
            },
        },
        404: {
            "description": "Отсутствие заказа",
            "content": {"application/json": {"example": {"detail": "Заказ не найден"}}},
        },
    },
)
async def get_order(
    order_id: str,
    _auth=Depends(security),
    async_session: "AsyncSession" = Depends(get_async_db_session),
    user: "Users" = Depends(get_current_user),
) -> Order:
    unique_key: str = f"{order_id}-{user.id}"
    _, data = await redis_client.check_cache(unique_key)
    if data:
        order = Order.model_validate_json(data)
    else:
        order = await get_order_by_id(order_id, async_session)
        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден"
            )
        await redis_client.add_to_cache(unique_key, Order.model_validate(order).model_dump(), settings.REDIS_TTL_EXPIRE)
    return order


@router.patch(
    "/{order_id}/",
    description="Поменять статус заказа",
    responses={
        200: {"description": "Успешное изменение", "model": Order},
        401: {
            "description": "Ошибки авторизации",
            "content": {
                "application/json": {"example": {"detail": "Токен не валиден"}}
            },
        },
        404: {
            "description": "Отсутствие заказа",
            "content": {"application/json": {"example": {"detail": "Заказ не найден"}}},
        },
    },
)
async def update_order_status(
    order_id: str,
    updated_data: OrderUpdate,
    _auth=Depends(security),
    async_session: "AsyncSession" = Depends(get_async_db_session),
    user: "Users" = Depends(get_current_user),
) -> Order:
    order = await get_order_by_id(order_id, async_session)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден"
        )
    order.status = updated_data.status
    await async_session.commit()
    await async_session.refresh(order)

    unique_key = f"{order_id}-{user.id}"
    check_cache = await redis_client.check_cache(unique_key)
    if check_cache:
        order_as_pydantic = Order.model_validate(order)
        await redis_client.add_to_cache(unique_key, order_as_pydantic.model_dump(), settings.REDIS_TTL_EXPIRE)

    return order


@router.get(
    "/user/{user_id}/",
    description="Получить заказы конкретного пользователя",
    responses={
        200: {
            "description": "Заказы пользователя",
            "model": list[Order],
        },
        401: {
            "description": "Ошибки авторизации",
            "content": {
                "application/json": {"example": {"detail": "Токен не валиден"}}
            },
        },
    },
)
async def get_users_orders(
    user_id: str,
    _auth=Depends(security),
    async_session: "AsyncSession" = Depends(get_async_db_session),
    _: "Users" = Depends(get_current_user),
) -> list[Order]:
    return await get_orders(async_session, user_id)
