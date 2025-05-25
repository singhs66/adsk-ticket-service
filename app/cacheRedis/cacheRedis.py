import redis
import json

redis_client = redis.Redis(host="clustercfg.ticket-service-cache.ujqbad.use1.cache.amazonaws.com", port=6379, decode_responses=True)


def cache_list_tickets() -> list:
    cached = redis_client.get("tickets")
    if cached:
        return json.loads(cached)

    serialized = [t.to_dict() for t in tickets]
    redis_client.setex("tickets", 6000, json.dumps(serialized))  # cache for 6000s
    
    return serialized



