from uuid import uuid4
from app.daoLayer.serviceObjects.TicketSO import TicketSO
from app.daoLayer.database import create_ticket_dao, list_ticket_dao, get_ticket_dao, \
    delete_ticket_dao, update_ticket_dao


def create_ticket(data):
    ticket_id = str(uuid4())
    ticket = TicketSO(**data.model_dump())
    ticket.id = ticket_id

    print("ticket details -----", ticket)

    create_ticket_dao(ticket)
    return ticket


def get_all_tickets():
    return list_ticket_dao()


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
