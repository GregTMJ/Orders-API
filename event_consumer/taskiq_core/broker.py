"""Модуль работы с RMQ брокером TaskIQ"""

from taskiq_aio_pika.broker import AioPikaBroker

from configs import settings

broker = AioPikaBroker(url=settings.RMQ_URL)
