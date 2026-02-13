from typing import Annotated, Literal
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings


class Configs(BaseSettings):
    # Настройки логирования
    LOGLEVEL: Annotated[
        Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], Field("INFO")
    ]

    # Настройки подключения к основной базе данных.
    POSTGRES_HOST: Annotated[str, Field("postgres")]
    POSTGRES_PORT: Annotated[int, Field(5432)]
    POSTGRES_DB: Annotated[str, Field("orders_user")]
    POSTGRES_PASSWORD: Annotated[str, Field("LyhaEkM2D6TeH96W8jxG")]
    POSTGRES_USER: Annotated[str, Field("orders_user")]
    POSTGRES_TRANSACTION_TIMEOUT: Annotated[int, Field(30)]
    POSTGRES_ECHO: Annotated[bool, Field(False)]

    # Настройки rabbitmq
    RMQ_USER: Annotated[str, Field("user")]
    RMQ_PASSWORD: Annotated[str, Field("bitnami")]
    RMQ_HOST: Annotated[str, Field("localhost")]
    RMQ_PORT: Annotated[int, Field("5672")]
    RMQ_VHOST: Annotated[str, Field("%2F")]
    RMQ_PARAMS: Annotated[str, Field("connection_attempts=3&heartbeat=60")]

    RMQ_EXCHANGE: Annotated[str, Field("test")]
    RMQ_QUEUE: Annotated[str, Field("test")]

    # Настройки Redis
    REDIS_HOST: Annotated[str, Field("")]
    REDIS_PORT: Annotated[int, Field(6379)]
    REDIS_USER: Annotated[str, Field("user")]
    REDIS_PASSWORD: Annotated[str, Field("12345")]
    REDIS_USER_PASSWORD: Annotated[str, Field("12345")]
    REDIS_TTL_EXPIRE: Annotated[int, Field(15)]

    # Настройки Токена
    JWT_SECRET_KEY: Annotated[str, Field("Somesecretkey")]
    JWT_ALGORITHM: Annotated[str, Field("HS256")]
    JWT_LIFETIME: Annotated[int, Field(10)]

    # Настройки проекта
    ENV_ALLOWED_ORIGINS: Annotated[str, Field("*")]

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

    @computed_field
    @property
    def POSTGRES_URL(self) -> str:
        """Метод формирования url для базы данных.

        Returns:
            str: URL для подключения к Postgres.
        """
        url = (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
        return url

    @computed_field
    @property
    def REDIS_URL(self) -> str:
        """Метод формирования url для Redis

        Returns:
            str: URL для подключения к Redis
        """
        return f"redis://{self.REDIS_USER}:{self.REDIS_USER_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}"

    @computed_field
    @property
    def ALLOWED_ORIGINS(self) -> list[str]:
        """Метод формирования допустимых доменов для работы с сервисом.

        Returns:
            list[str]: Список из доменов
        """
        return self.ENV_ALLOWED_ORIGINS.split(",")


settings = Configs()
