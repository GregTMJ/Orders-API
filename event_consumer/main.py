"""Основной метод вызова приложения"""
from faststream.asgi import AsgiFastStream, make_ping_asgi

from faststream_core.broker import broker
from taskiq_core.broker import broker as taskiq_broker

app = AsgiFastStream(
    broker,
    asgi_routes=[
        ("/health", make_ping_asgi(broker, timeout=5.0)),
    ],
    asyncapi_path="/docs",
)


@app.after_startup
async def taskiq_broker_start():
    """Метод для подключения taskiq worker после старта FastStream"""
    if not taskiq_broker.is_worker_process:
        await taskiq_broker.startup()


@app.after_shutdown
async def taskiq_broker_stop():
    """Метода отключения taskiq worker после отключения FastStream"""
    if taskiq_broker.is_worker_process:
        await taskiq_broker.shutdown()
