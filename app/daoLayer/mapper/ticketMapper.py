from app.daoLayer.dataModel.ticketDO import Ticket
from app.daoLayer.serviceObjects import TicketSO


def ticketMapper(ticketSO: TicketSO) -> Ticket:
    db_ticket = Ticket(
        id=ticketSO.id,
        title=ticketSO.title,
        description=ticketSO.description,
        status=ticketSO.status,
        severity=ticketSO.severity)
    return db_ticket
