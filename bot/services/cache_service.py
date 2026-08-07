"""
Cache service supporting Redis with transparent in-memory fallback.
"""
from typing import Optional, Any
import json
from bot.config.settings import settings
from bot.utils.logger import logger

try:
    import redis.asyncio as redis
    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False


class CacheService:
    def __init__(self):
        self._redis: Optional[Any] = None
        self._memory_cache: dict[str, Any] = {}

    async def initialize(self) -> None:
        if HAS_REDIS and settings.REDIS_URL:
            try:
                self._redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
                await self._redis.ping()
                logger.info("Connected to Redis cache successfully.")
                return
            except Exception as e:
                logger.warning(f"Failed to connect to Redis ({e}). Falling back to in-memory cache.")
                self._redis = None
        logger.info("Using in-memory dictionary cache.")

    async def get(self, key: str) -> Optional[Any]:
        if self._redis:
            val = await self._redis.get(key)
            if val is not None:
                try:
                    return json.loads(val)
                except Exception:
                    return val
            return None
        return self._memory_cache.get(key)

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        serialized = json.dumps(value) if isinstance(value, (dict, list)) else str(value)
        if self._redis:
            if ttl:
                await self._redis.setex(key, ttl, serialized)
            else:
                await self._redis.set(key, serialized)
        else:
            self._memory_cache[key] = value

    async def delete(self, key: str) -> None:
        if self._redis:
            await self._redis.delete(key)
        else:
            self._memory_cache.pop(key, None)

    async def close(self) -> None:
        if self._redis:
            await self._redis.close()


cache_service = CacheService()
