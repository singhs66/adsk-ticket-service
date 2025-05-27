import datetime
import random
import json
import uuid
from uuid import uuid4

from app.apiSchemas import TicketCreate
from app.daoLayer.serviceObjects.TicketSO import TicketSO
from app.daoLayer.database import create_ticket_dao, list_ticket_dao, get_ticket_dao, \
    delete_ticket_dao, update_ticket_dao
from app.cacheRedis import RedisCache


def create_ticket(data: TicketCreate):
    ticket_id = uuid4()
    ticketSO = TicketSO(
        id=ticket_id,
        title=data.title,
        description=data.description,
        severity=data.severity or "medium",
        status=data.status or "Open",
        assignee=assign_tickets_randomly(),
        created_at=datetime.datetime.now(),
        category=data.category)

    ticketSO.id = ticket_id

    print("ticket details -----", ticketSO)

    create_ticket_dao(ticketSO)
    return ticketSO


def serialize_ticket(t):
    """
    Serializes a ticket object to a dictionary for caching.
    Tries model_dump (Pydantic v2), then dict (Pydantic v1), then __dict__, then str as fallback.
    Removes SQLAlchemy InstanceState if present.
    Converts UUID and datetime fields to strings for JSON serialization.
    """
    def convert(obj):
        if isinstance(obj, dict):
            return {k: convert(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert(i) for i in obj]
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        else:
            return obj
    if hasattr(t, 'model_dump'):
        d = t.model_dump()
    elif hasattr(t, 'dict'):
        d = t.dict()
    elif hasattr(t, '__dict__'):
        d = dict(t.__dict__)
        d.pop('_sa_instance_state', None)
    else:
        d = str(t)
    return convert(d)


def get_all_tickets(status: str ,
                    sort_by: str,
                    assignee: str):
    cache_key = f"tickets:all:{status}:{sort_by}:{assignee}"
    print(f"[RedisCache] Checking cache for key: {cache_key}")
    cached = RedisCache.get(cache_key)
    if cached:
        print(f"[RedisCache] Cache hit for key: {cache_key}")
        return json.loads(cached)
    print(f"[RedisCache] Cache miss for key: {cache_key}. Fetching from DB and setting cache.")
    result = list_ticket_dao(status, sort_by, assignee)
    RedisCache.set(cache_key, json.dumps([serialize_ticket(t) for t in result]))
    print(f"[RedisCache] Cache set for key: {cache_key}")
    return result


def get_ticket(ticket_id):
    cache_key = f"ticket:{ticket_id}"
    print(f"[RedisCache] Checking cache for key: {cache_key}")
    cached = RedisCache.get(cache_key)
    if cached:
        print(f"[RedisCache] Cache hit for key: {cache_key}")
        return json.loads(cached)
    print(f"[RedisCache] Cache miss for key: {cache_key}. Fetching from DB and setting cache.")
    result = get_ticket_dao(ticket_id)
    if result:
        data = serialize_ticket(result)
        RedisCache.set(cache_key, json.dumps(data))
        print(f"[RedisCache] Cache set for key: {cache_key}")
    return result


def update_ticket(ticket_id, data):
    result = update_ticket_dao(ticket_id, data)
    # Invalidate cache for this ticket and ticket list
    print(f"[RedisCache] Invalidating cache for ticket:{ticket_id}")
    RedisCache.get_client().delete(f"ticket:{ticket_id}")
    # If your app allows filtering/sorting on the ticket list, it is better to invalidate all relevant caches (e.g., all keys matching tickets:all:*)
    # This deletes only the cache for the default/unfiltered ticket list (status=None, sort_by=created_at, assignee=None)
    print(f"[RedisCache] Invalidating cache for tickets:all:None:created_at:None")
    RedisCache.get_client().delete("tickets:all:None:created_at:None")
    return result


def delete_ticket(ticket_id):
    result = delete_ticket_dao(ticket_id)
    # Invalidate cache for this ticket and ticket list
    print(f"[RedisCache] Invalidating cache for ticket:{ticket_id}")
    RedisCache.get_client().delete(f"ticket:{ticket_id}")
    # If your app allows filtering/sorting on the ticket list, it is better to invalidate all relevant caches (e.g., all keys matching tickets:all:*)
    # This deletes only the cache for the default/unfiltered ticket list (status=None, sort_by=created_at, assignee=None)
    print(f"[RedisCache] Invalidating cache for tickets:all:None:created_at:None")
    RedisCache.get_client().delete("tickets:all:None:created_at:None")
    return result



def assign_tickets_randomly() -> str:
    """
        Assigns each ticket to a random user from the provided list.
        Modifies tickets in-place with a new 'assignee' field.
        """
    assignees = [
        "Alice Johnson",
        "Bob Smith",
        "Carol Lee",
        "David Wright",
        "Emma Brown",
        "Frank Harris",
        "Grace Patel",
        "Henry Clark",
        "Isla Nguyen",
        "Jack Martinez"
    ];

    random.shuffle(assignees)
    return assignees[0]

