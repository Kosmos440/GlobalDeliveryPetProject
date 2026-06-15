import redis.asyncio as aioredis
from app.core.config import settings


cache_client = aioredis.from_url(settings.REDIS_CACHE)
broker_client = aioredis.from_url(settings.REDIS_BROKER)
