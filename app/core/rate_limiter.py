import time
from app.core.redis import redis_client

def rate_limit(
    key: str,
    limit: int,
    window_seconds: int
):
    current = redis_client.get(key)

    if current is None:
        redis_client.set(key, 1, ex=window_seconds)
        return True

    if int(current) >= limit:
        return False

    redis_client.incr(key)
    return True
