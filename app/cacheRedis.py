from datetime import datetime
from uuid import UUID

import redis
import json

from app.daoLayer.serviceObjects.TicketSO import TicketSO

redis_client = redis.Redis(host="clustercfg.ticket-service-cache.ujqbad.use1.cache.amazonaws.com", port=6379,
                           decode_responses=True)
REDIS_TTL = int(100)

def get_from_cache(key: str):
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)
    return None

def set_to_cache(key: str, value: TicketSO, ttl: int = REDIS_TTL):
    try:
        cache_is_working = redis_client.ping()
        print('I am Redis. Try me. I can remember things, only for a short time though :)')
    except Exception as e:
        print('EXCEPTION: host could not be accessed ---> ', repr(e))
    # print("cache value ->>>", value)
    # redis_client.setex(key, ttl, "serialized")
    # try:
    #     serialized = json.dumps(value, cls=EnhancedEncoder)
    #     print("Added to cache")
    #     redis_client.setex(key, ttl, serialized)
    #     print("Added to cache")
    # except Exception as e:
    #     print(f"[cache-error] Failed to serialize key={key} :: {e}")

def invalidate_cache(key: str):
    redis_client.delete(key)


class EnhancedEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if hasattr(obj, "model_dump"):
            return obj.model_dump(mode="json")
        return super().default(obj)






import asyncio
#
# from glide import (
#     ClosingError,
#     ConnectionError,
#     GlideClusterClient,
#     GlideClusterClientConfiguration,
#     Logger,
#     LogLevel,
#     NodeAddress,
#     RequestError,
#     TimeoutError,
# )

# async def main():
#     # Set logger configuration
#     Logger.set_logger_config(LogLevel.INFO)
#
#     # Configure the Glide Cluster Client
#     addresses = [
#         NodeAddress("clustercfg.ticket-service-cache.ujqbad.use1.cache.amazonaws.com", 6379)
#     ]
#     config = GlideClusterClientConfiguration(addresses=addresses, use_tls=True)
#     client = None
#
#     try:
#         print("Connecting to Valkey Glide...")
#
#         # Create the client
#         client = await GlideClusterClient.create(config)
#         print("Connected successfully.")
#
#         # Perform SET operation
#         result = await client.set("key", "value")
#         print(f"Set key 'key' to 'value': {result}")
#
#         # Perform GET operation
#         value = await client.get("key")
#         print(f"Get response for 'key': {value}")
#
#         # Perform PING operation
#         ping_response = await client.ping()
#         print(f"PING response: {ping_response}")
#
#     except (TimeoutError, RequestError, ConnectionError, ClosingError) as e:
#         print(f"An error occurred: {e}")
#     finally:
#         # Close the client connection
#         if client:
#             try:
#                 await client.close()
#                 print("Client connection closed.")
#             except ClosingError as e:
#                 print(f"Error closing client: {e}")
#
#
# asyncio.run(main())