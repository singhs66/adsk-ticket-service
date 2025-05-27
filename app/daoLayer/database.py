from http.client import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import boto3
import os

from app import apiSchemas
from app.apiSchemas import TicketUpdate
from app.daoLayer.dataModel.ticketDO import Ticket
from app.daoLayer.database_base import Base
from app.daoLayer.mapper.ticketMapper import ticketMapper
from app.daoLayer.serviceObjects import TicketSO
from sqlalchemy import text
from app.integrations.slackbot.slackbot import send_slack_notification_create


# Get DB password: use env var in AWS, fetch from SSM for local/dev
DB_PASSWORD = os.getenv("DB_PASSWORD")
if not DB_PASSWORD:
    # Only fetch from SSM if NOT running in ECS
    if not os.getenv("ECS_CONTAINER_METADATA_URI") and not os.getenv("AWS_EXECUTION_ENV"):
        DB_PASSWORD_PARAM = os.getenv("DB_PASSWORD_PARAM_NAME", "/fastapi/production/db_password")
        AWS_REGION = os.getenv("AWS_REGION", "us-west-2")
        import boto3
        def get_db_password_from_ssm(param_name: str, region: str = "us-west-2"):
            ssm = boto3.client("ssm", region_name=region)
            response = ssm.get_parameter(Name=param_name, WithDecryption=True)
            return response["Parameter"]["Value"]
        DB_PASSWORD = get_db_password_from_ssm(DB_PASSWORD_PARAM, region=AWS_REGION)
    else:
        raise RuntimeError("DB_PASSWORD environment variable is not set in ECS. Check your ECS secrets configuration.")

DATABASE_URL = f"postgresql://postgres:{DB_PASSWORD}@database-1.cqdw0cis8jds.us-east-1.rds.amazonaws.com:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine, checkfirst=True)
    create_indexes()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_ticket_dao(ticketSO: TicketSO):
    db = SessionLocal()
    try:
        db_ticket = ticketMapper(ticketSO)
        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)

        # Add new ticket to cache
        # set_to_cache(ticketSO.id, ticketSO)

        # Add Slack notification when ticket is created
        send_slack_notification_create(ticketSO, action="Created")

        return db_ticket
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def list_ticket_dao(status: str ,
                    sort_by: str,
                    assignee: str):
    db = SessionLocal()
    try:
        query = db.query(Ticket)
        # Index on `status`
        print(status,"status value")
        if status:
            query = query.filter(Ticket.status == status)

        print(assignee, "assignee value")
        if assignee:
            query = query.filter(Ticket.assignee == assignee)

        # Query all records from the tickets table
        listTicketSO = query.all()
        finalListTicketSO = [ticket for ticket in listTicketSO]
        return finalListTicketSO

    finally:
        # Close the session
        db.close()


def get_ticket_dao(ticket_id: str):
    db = SessionLocal()
    # Check this in cache
    # cached = get_from_cache(ticket_id)
    # if cached:
    #     return cached
    try:
        # Query ticket_id record from the tickets table
        getTicketSO = db.query(Ticket).filter(Ticket.id == ticket_id).first()

        # Add this to cache
        # set_to_cache(ticket_id, getTicketSO)
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
        if updatedTicket.status:
            db_ticket.status = updatedTicket.status
        if updatedTicket.description:
            db_ticket.description = updatedTicket.description
        print("Successfully Updated --> ", db_ticket)
        db.commit()
        db.refresh(db_ticket)

        print("After commit →", db_ticket.status, db_ticket.description)

        send_slack_notification_create(db_ticket, action="Updated")

        # Invalidate your existing cache record and update
        # with the latest ticket details
        # invalidate_cache(ticket_id)
        # set_to_cache(ticket_id, db_ticket)

        return db_ticket
    finally:
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

# Creating indexes using status and reporter
def create_indexes():
    sql_statements = [
        'CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);',
        'CREATE INDEX IF NOT EXISTS idx_tickets_created_at ON tickets(created_at DESC);',
        'CREATE INDEX IF NOT EXISTS idx_tickets_reporter ON tickets(id);'
        'CREATE INDEX IF NOT EXISTS idx_tickets_assignee ON tickets(assignee);'
    ]

    db = SessionLocal()
    try:
        for stmt in sql_statements:
            db.execute(text(stmt))
        db.commit()
        print("Indexes created successfully")
    except Exception as e:
        db.rollback()
        print("Error creating indexes:", e)
    finally:
        db.close()
