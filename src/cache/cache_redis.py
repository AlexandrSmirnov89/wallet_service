import asyncio

import redis.asyncio as redis
from src.core.config import settings

redis_client = None  # Глобальная переменная для кеша

async def get_redis():
    global redis_client
    if redis_client is None:
        redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
    return redis_client

async def set_cache(wallet_id: str, balance: float):
    print(f"сохраняю кэш - wallet:{wallet_id}")
    redis_client = await get_redis()
    await redis_client.set(f"wallet:{wallet_id}", str(balance), ex=60)

async def get_cache(wallet_id: str):
    """Получаем баланс из кеша Redis"""
    redis_client = await get_redis()
    balance = await redis_client.get(f"wallet:{wallet_id}")
    return float(balance) if balance else None
