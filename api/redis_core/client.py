"""Модуль работы с Redis."""
from redis import asyncio as aioredis
from redis.exceptions import NoScriptError
import logging

from helpers.orjson_coder import ORJsonCoder


class RedisClient:
    async def connect(self, redis_url: str) -> bool:
        """Метод подключения к Redis.

        Args:
            redis_url (str): Домен подключения

        Returns:
            bool: True в случае успешности, иначе False
        """
        self.pool = aioredis.ConnectionPool().from_url(redis_url)
        self.redis = aioredis.Redis.from_pool(self.pool)
        if await self.redis.ping():
            logging.info("Redis connected")
            return True
        logging.warning("Cannot connect to Redis")
        return False

    async def add_to_cache(self, key: str, value: dict, expire: int) -> bool:
        """Метод добавления данных в кэш.

        Args:
            key (str): Уникальный ключ
            value (dict): значение ключа
            expire (int): Время истечения хранения кэша (в сек)

        Returns:
            bool: True если сохранено, иначе False
        """
        try:
            response_data = ORJsonCoder.encode(value)
        except TypeError:
            message = f"Object of type {type(value)} is not JSON-serializable"
            logging.error(message)
            return False
        cached = await self.redis.set(name=key, value=response_data, ex=expire)
        if cached:
            logging.info(f"{key} added to cache")
        else:
            logging.warning(f"Failed to cache key {key}")
        return cached

    async def check_cache(self, key: str) -> tuple[int, str]:
        """Метод проверки наличие кэша по ключу

        Args:
            key (str): Уникальный ключ

        Returns:
            tuple[int, str]: Время жизни + само значение
        """
        async with self.redis.pipeline() as pipe:
            ttl, in_cache = await pipe.ttl(key).get(key).execute()
            if in_cache:
                logging.info(f"Key {key} found in cache")
            return ttl, in_cache

    async def disconnect(self):
        """Метод закрытыя соединения с Redis"""
        if await self.redis.ping():
            await self.redis.aclose()
            logging.info("Redis disconnected")
        return None

    @staticmethod
    def decode_cache(data: str):
        """Метод декодирования данных."""
        return ORJsonCoder.decode(data)

    async def ping(self):
        """Проверка работы клиента."""
        if await self.redis.ping():
            return True
        return False

    async def load_script(self, script: str):
        """Метод использования скриптов Lua для работы с Redis.

        Args:
            script (str): Скрипт из Lua
        """
        return await self.redis.script_load(script)

    async def evaluate_sha(self, sha: str, keys_len: int, values=None):
        if values is None:
            values = []
        return await self.redis.evalsha(sha, keys_len, *values)


redis_client = RedisClient()
