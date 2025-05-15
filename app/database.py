from app import apiSchemas

ticket = apiSchemas.TicketResponse

ticket.id = "1"
ticket.status = "progress"
ticket.title = "some"
ticket.description = "description"
ticket.priority = "high"

d = {ticket.id: ticket}


def tickets_db():
    return d
