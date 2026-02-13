"""Модуль ридеректа"""

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="", include_in_schema=False)


@router.get("/")
async def redirect_docs():
    return RedirectResponse(url="/docs")
