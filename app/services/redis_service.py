import redis
import json
from app.config import settings

# Initialize Redis client
redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

def get_cached_answer(question: str, owner_id: int | None) -> dict | None:
    cache_key = f"rag_cache:{owner_id}:{question.strip().lower()}"
    try:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
    except Exception:
        # Fail gracefully if Redis is offline
        pass
    return None

def set_cached_answer(question: str, owner_id: int | None, result: dict, expire_seconds: int = 3600):
    cache_key = f"rag_cache:{owner_id}:{question.strip().lower()}"
    try:
        redis_client.setex(cache_key, expire_seconds, json.dumps(result))
    except Exception:
        pass