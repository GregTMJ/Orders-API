"""Модуль работы с брокером FastStream"""

from faststream import Logger
from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitMessage, RabbitQueue

from configs import settings

from taskiq_core.tasks import process_order

broker = RabbitBroker(url=settings.RMQ_URL)


@broker.subscriber(
    queue=RabbitQueue(
        name=settings.RMQ_QUEUE,
        durable=True,
    ),
    exchange=RabbitExchange(name=settings.RMQ_EXCHANGE, durable=True),
)
async def handle_task(message: RabbitMessage, logger: Logger):
    """Саб для обработки сообщения по конфигам выше.

    Args:
        message (RabbitMessage): Приходящее сообщение как сущность FastStream.
        logger (Logger): Логирование из контекста FastStream.
    """
    headers = message.headers
    if headers.get("task_name") != "new_order":
        logger.warning(f"Ignore message {message.body}")
        return

    incoming_message: dict = await message.decode()
    order_id = incoming_message.get("order_id")
    if order_id is None:
        logger.warning("No order ID was given")
        return

    await process_order.kiq(order_id)
    logger.info("Message sent to taskiq")
