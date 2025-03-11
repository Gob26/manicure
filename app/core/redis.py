from redis.asyncio import Redis as AsyncRedis
from typing import Optional
# Импортируем redis_config напрямую из модуля redis
from config.components.redis import redis_config

_redis_client: Optional[AsyncRedis] = None

def get_redis_client() -> AsyncRedis:
    """
    Получить асинхронный клиент Redis. Использует паттерн Singleton для создания единственного клиента.
    """
    global _redis_client
    if _redis_client is None:
        _redis_client = AsyncRedis.from_url(redis_config.redis_connection_string, decode_responses=True)
    return _redis_client