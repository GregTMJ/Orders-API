"""модуль работы с RMQ"""

from typing import TYPE_CHECKING
from aio_pika import ExchangeType, DeliveryMode, Message, connect_robust

from helpers.logger import logger

if TYPE_CHECKING:
    from aio_pika import RobustConnection


class RMQClient:
    def __init__(self):
        self._connection: "RobustConnection" = None

    async def connect(self, rmq_url: str, **kwargs) -> "RobustConnection":
        """Метод подключения к RMQ серверу."""
        self._connection = await connect_robust(rmq_url, **kwargs)
        logger.info("Connected to RMQ")
        return self._connection

    async def send_message(
        self, exchange_name: str, queue_name: str, message: str, task_name: str
    ):
        """Метод отправки сообщений в RMQ по переданным параметрам

        Args:
            exchange_name (str): Название обменника
            queue_name (str): Название очереди
            message (str): Содержание сообщений в формате json
            task_name (Str): Название задачи по event-bus
        """
        async with self._connection:
            channel = await self._connection.channel()

            exchange = await channel.declare_exchange(
                name=exchange_name, type=ExchangeType.DIRECT, durable=True
            )
            queue = await channel.declare_queue(name=queue_name, durable=True)
            await queue.bind(exchange, routing_key=queue_name)
            message = Message(
                body=message.encode(),
                delivery_mode=DeliveryMode.PERSISTENT,
                headers={"task_name": task_name, "content-type": "application/json"},
            )
            await exchange.publish(message, routing_key=queue_name)
            logger.info(f"Message sent to {exchange_name}-{queue_name}")

    async def disconnect(self):
        """Метод закрытия соединения."""
        if self._connection:
            await self._connection.close()
        logger.info("RMQ disconnected")


rmq_client = RMQClient()
