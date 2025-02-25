import redis.asyncio as async_redis
import redis
from src.core.config import settings

redis_client = None
sync_redis = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

async def get_async_redis():
    global redis_client
    if redis_client is None:
        redis_client = async_redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
    return redis_client

async def set_async_cache(wallet_id: str, balance: float):
    redis_client = await get_async_redis()
    await redis_client.set(f"wallet:{wallet_id}", str(balance), ex=60)

async def get_async_cache(wallet_id: str):
    redis_client = await get_async_redis()
    balance = await redis_client.get(f"wallet:{wallet_id}")
    return float(balance) if balance else None

def set_sync_cache(wallet_id: str, balance: float):
    sync_redis.set(f"wallet:{wallet_id}", str(balance), ex=60)

def get_sync_cache(wallet_id: str):
    balance = sync_redis.get(f"wallet:{wallet_id}")
    return float(balance) if balance else None