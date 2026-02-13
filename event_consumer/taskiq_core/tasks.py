"""Модуль описания фоновых задач"""

import asyncio

from .broker import broker


@broker.task
async def process_order(order_id: str) -> None:
    """Таска работы с приходящим заказом."""
    await asyncio.sleep(2)
    print(f"Order {order_id} processed")
