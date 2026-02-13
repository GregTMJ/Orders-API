from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from configs import settings
from database.connection import healthcheck as db_healthcheck
from helpers.logger import init_logger
from rabbit_core.client import rmq_client
from redis_core.client import redis_client
from routers.auth import router as auth_router
from routers.orders import router as order_router
from routers.ping import router as ping_router
from routers.redirect import router as redirect_router


@asynccontextmanager
async def lifespan(app_: "FastAPI"):
    """
    Контекст запуска элементов, используемые в проекте такие как: Redis, TaskIQ и т.д.
    """
    init_logger()
    # Инициализация коннекта в Redis
    await redis_client.connect(settings.REDIS_URL)
    # HealthCheck БД
    await db_healthcheck()
    # Подключение к RMQ
    await rmq_client.connect(settings.RMQ_URL)
    yield

    # Отключения от внешних сервисов
    await rmq_client.disconnect()
    await redis_client.disconnect()


app = FastAPI(
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(redirect_router)
app.include_router(ping_router)
app.include_router(auth_router)
app.include_router(order_router)
