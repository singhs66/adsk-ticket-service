import datetime
import random
from typing import List
from uuid import uuid4

from app.apiSchemas import TicketCreate
from app.daoLayer.serviceObjects.TicketSO import TicketSO
from app.daoLayer.database import create_ticket_dao, list_ticket_dao, get_ticket_dao, \
    delete_ticket_dao, update_ticket_dao


def create_ticket(data: TicketCreate):
    ticket_id = uuid4()
    ticketSO = TicketSO(
        id=ticket_id,
        title=data.title,
        description=data.description,
        severity=data.severity or "medium",
        assignee=assign_tickets_randomly(),
        created_at=datetime.datetime.now(),
        category=data.category)

    ticketSO.id = ticket_id

    print("ticket details -----", ticketSO)

    create_ticket_dao(ticketSO)
    return ticketSO


def get_all_tickets(status: str ,
                    sort_by: str,
                    assignee: str):
    return list_ticket_dao(status, sort_by, assignee)


def get_ticket(ticket_id):
    return get_ticket_dao(ticket_id)


def update_ticket(ticket_id, data):
    # getTicketSO = get_ticket_dao(ticket_id)
    # if not getTicketSO:
    #     return None
    # updatedTicketSO = getTicketSO.copy(update=data.dict(exclude_unset=True))
    return update_ticket_dao(ticket_id,data)


def delete_ticket(ticket_id):
    return delete_ticket_dao(ticket_id)



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

