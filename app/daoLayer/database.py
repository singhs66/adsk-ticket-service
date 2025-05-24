from http.client import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import apiSchemas
from app.apiSchemas import TicketUpdate
from app.daoLayer.dataModel.ticketDO import Ticket
from app.daoLayer.database_base import Base
from app.daoLayer.mapper.ticketMapper import ticketMapper
from app.daoLayer.serviceObjects import TicketSO


def buildLocalDB():
    localTicket = apiSchemas.TicketResponse
    localTicket.id = "1"
    localTicket.status = "progress"
    localTicket.title = "some"
    localTicket.description = "description"
    localTicket.severity = "high"

    return {localTicket.id: localTicket}


DATABASE_URL = "postgresql://postgres:nikhiltest@database-1.cqdw0cis8jds.us-east-1.rds.amazonaws.com:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine, checkfirst=True)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def tickets_db():
    return buildLocalDB()


def create_ticket_dao(ticketSO: TicketSO):
    db = SessionLocal()
    try:
        db_ticket = ticketMapper(ticketSO)
        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)
        return db_ticket
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def list_ticket_dao():
    db = SessionLocal()
    try:
        # Query all records from the tickets table
        listTickets = db.query(Ticket).all()
        list_tickets = [ticket for ticket in listTickets]
        return list_tickets

    finally:
        # Close the session
        db.close()


def get_ticket_dao(ticket_id: str):
    db = SessionLocal()
    try:
        # Query ticket_id record from the tickets table
        getTicketSO = db.query(Ticket).get(ticket_id)

        return getTicketSO

    finally:
        # Close the session
        db.close()


def update_ticket_dao(ticket_id: str, updatedTicket: TicketUpdate):
    db = SessionLocal()
    try:
        print(updatedTicket , "updating value")
        db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not db_ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        print("Updated --> ", updatedTicket)
        for key, value in updatedTicket.dict().items():
            setattr(db_ticket, key, value)
        db.commit()
        db.refresh(db_ticket)
    finally:
        # Close the session
        db.close()


def delete_ticket_dao(ticket_id: str):
    db = SessionLocal()
    try:

        deleted = db.query(Ticket).filter(Ticket.id == ticket_id).delete(synchronize_session="fetch")
        db.commit()
        if deleted == 0:
            raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")
        print("Deleted the ticket successfully ->", ticket_id)
        return True
    except Exception as e:
        db.rollback()
        print("Error deleting ticket:", e)
        raise HTTPException(status_code=500, detail="Failed to delete ticket")
