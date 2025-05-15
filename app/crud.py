from uuid import uuid4
from app.TicketSO import TicketSO
from app.database import tickets_db


def create_ticket(data):
    ticket_id = str(uuid4())
    ticket = TicketSO(id=ticket_id, **data.dict())

    database = tickets_db()
    database[ticket_id] = ticket
    return ticket


def get_all_tickets():
    return list(tickets_db().values())


def get_ticket(ticket_id):
    return tickets_db().get(ticket_id)


def update_ticket(ticket_id, data):
    ticket = tickets_db.get(ticket_id)
    if not ticket:
        return None
    updated = ticket.copy(update=data.dict(exclude_unset=True))
    tickets_db[ticket_id] = updated
    return updated


def delete_ticket(ticket_id):
    return tickets_db.pop(ticket_id, None)
