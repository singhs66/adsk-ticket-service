# Redis Caching & Testing Guide for FastAPI Ticketing System

This guide explains how to set up, test, and verify Redis caching and cache invalidation in your FastAPI backend, both locally and on AWS ElastiCache.

---

## Redis Data Flow Diagrams

Below are simple data flow diagrams illustrating how Redis caching is integrated into the ticketing system for both single ticket and ticket list queries.

### 1. Single Ticket Fetch (Cache-Aside Pattern)

```
[Client] 
   |
   v
[API Endpoint] 
   |
   v
[Check Redis: ticket:{id}]
   |         \
   | (Hit)    \ (Miss)
   v           v
[Return]   [Query DB]
   |           |
   |           v
   |     [Store in Redis: ticket:{id}]
   |           |
   +-----------+
   |
[Return to Client]
```

---

### 2. Ticket List Fetch (with Filters)

```
[Client]
   |
   v
[API Endpoint]
   |
   v
[Check Redis: tickets:all:{status}:{sort_by}:{assignee}]
   |         \
   | (Hit)    \ (Miss)
   v           v
[Return]   [Query DB with filters]
   |           |
   |           v
   |     [Store in Redis: tickets:all:{status}:{sort_by}:{assignee}]
   |           |
   +-----------+
   |
[Return to Client]
```

---

**Note:**  
- On ticket creation, update, or delete, the relevant Redis keys are invalidated or updated to keep cache and database in sync.
- This cache-aside pattern ensures the system always serves fresh data and improves performance for frequent queries.


---

---

## 1. Ensure Redis is Running (Local)

If you haven’t already, start Redis:
```bash
brew services start redis
```
Or, to run manually:
```bash
redis-server
```

---

## 2. Start Your FastAPI App

In your project directory:
```bash
uvicorn main:app --reload
```

---

## 3. Test the Ticket List Endpoint (Cache Set & Hit)

- Use curl, Postman, or your browser to call the ticket list endpoint:
  ```bash
  curl "http://127.0.0.1:8000/tickets"
  ```
- The first call should fetch from the database and set the cache.
- Call the same endpoint again. This time, the result should come from Redis (cache hit).

**Tip:**
Add a print/log statement in your `RedisCache.get` and `set` methods to confirm cache hits/misses.

---

## 4. Test Cache Invalidation (Update/Delete)

- Update a ticket:
  ```bash
  curl -X PUT "http://127.0.0.1:8000/tickets/<ticket_id>" -H "Content-Type: application/json" -d '{"title": "Updated title"}'
  ```
- Or delete a ticket:
  ```bash
  curl -X DELETE "http://127.0.0.1:8000/tickets/<ticket_id>"
  ```
- After updating or deleting, call the ticket list endpoint again:
  ```bash
  curl "http://127.0.0.1:8000/tickets"
  ```
- The cache for the ticket list should be invalidated, and you should see fresh data.

---

## 5. Test with AWS ElastiCache Redis

- Ensure your `REDIS_URL` is set to your ElastiCache endpoint in your environment or ECS task definition.
- Use the production API endpoint:
  ```bash
  curl -X GET "https://www.adskticket.com/tickets" \
    -H "accept: application/json" \
    -H "Authorization: Bearer <ACCESS_TOKEN>"
  ```
- Repeat the request within 10 minutes (default TTL) to observe cache hits.
- Use `/redis-health` endpoint to check Redis connectivity:
  ```bash
  curl -X GET "https://www.adskticket.com/redis-health" \
    -H "accept: application/json" \
    -H "Authorization: Bearer <ACCESS_TOKEN>"
  ```
- If you see repeated cache misses, check the TTL and Redis connection as described in troubleshooting.

---

## 6. (Optional) Inspect Redis Directly (AWS)

- SSH into an EC2 instance in the same VPC as ElastiCache.
- Connect using redis-cli:
  ```bash
  redis-cli -h <your-redis-endpoint> -p 6379
  keys tickets:*
  get tickets:all:None:created_at:None
  ```

---

## 7. Cache Expiry (TTL)

- The default cache TTL is **600 seconds (10 minutes)**. You can change this in `app/cacheRedis.py` by editing `CACHE_TTL_SECONDS`.
- If you see cache misses after 10 minutes, this is expected.

---

## 8. Troubleshooting

- Ensure all app instances use the same `REDIS_URL`.
- Check logs for cache hit/miss and Redis errors.
- Confirm no network/security group issues between ECS and ElastiCache.
- If using local Redis, make sure it is running and accessible.

---

## Summary
- First GET: populates cache
- Second GET: should hit cache
- Update/Delete: invalidates cache
- Next GET: fetches fresh data and resets cache

For more details, see the main README or the code comments in `app/crud.py`.
