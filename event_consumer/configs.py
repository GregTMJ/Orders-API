from typing import Annotated, Literal
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings


class Configs(BaseSettings):
    # Настройки логирования
    LOGLEVEL: Annotated[
        Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], Field("INFO")
    ]

    # Настройки rabbitmq
    RMQ_USER: Annotated[str, Field("user")]
    RMQ_PASSWORD: Annotated[str, Field("bitnami")]
    RMQ_HOST: Annotated[str, Field("localhost")]
    RMQ_PORT: Annotated[int, Field("5672")]
    RMQ_VHOST: Annotated[str, Field("%2F")]
    RMQ_PARAMS: Annotated[str, Field("connection_attempts=3&heartbeat=60")]

    RMQ_EXCHANGE: Annotated[str, Field("test")]
    RMQ_QUEUE: Annotated[str, Field("test")]

    @computed_field
    @property
    def RMQ_URL(self) -> str:
        """Метод формирования url для RabbitMQ.

        Returns:
            str: URL для подключения к RabbitMQ.
        """
        url = (
            f"amqp://{self.RMQ_USER}:{self.RMQ_PASSWORD}@{self.RMQ_HOST}:"
            f"{self.RMQ_PORT}/{self.RMQ_VHOST}?{self.RMQ_PARAMS}"
        )
        return url


settings = Configs()
