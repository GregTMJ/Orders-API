"""Модуль описание роутов пинга"""

from fastapi import APIRouter

router = APIRouter(prefix="", tags=["HealthCheck"])


@router.get("/ping/")
async def ping() -> str:
    return "pong"
