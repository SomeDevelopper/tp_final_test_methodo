import redis.asyncio as redis
import json
from src.config.config import settings

class RedisService:
    def __init__(self, redis_url: str = None):
        if redis_url:
            self.redis = redis.from_url(redis_url)
        else:
            self.redis = redis.from_url(settings.REDIS_URL)

    async def get(self, key):
        values = await self.redis.get(key)
        if values:
            return json.loads(values)
        return None
    
    async def set(self, key, value, ttl= 300):
        await self.redis.set(key, json.dumps(value), ex=ttl)