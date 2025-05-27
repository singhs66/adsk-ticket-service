from datetime import datetime
from uuid import UUID

import redis
import json
import os

CACHE_TTL_SECONDS = 600  # Cache expiry in seconds (10 minutes)

class EnhancedEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if hasattr(obj, "model_dump"):
            return obj.model_dump(mode="json")
        return super().default(obj)

class RedisCache:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            redis_url = os.getenv("REDIS_URL")
            if redis_url:
                cls._client = redis.Redis.from_url(redis_url, decode_responses=True)
            else:
                cls._client = redis.Redis(
                    host=os.getenv("REDIS_HOST", "localhost"),
                    port=int(os.getenv("REDIS_PORT", 6379)),
                    db=0,
                    decode_responses=True
                )
        return cls._client

    @classmethod
    def get(cls, key):
        return cls.get_client().get(key)

    @classmethod
    def set(cls, key, value, ex=CACHE_TTL_SECONDS):
        cls.get_client().set(key, value, ex=ex)

    @classmethod
    def ping(cls):
        try:
            return cls.get_client().ping()
        except Exception as e:
            print(f"Redis connection error: {e}")
            return False
