from fastapi import APIRouter, HTTPException
from app import crud
from app.daoLayer.serviceObjects.TicketSO import TicketSO
from app.apiSchemas import TicketCreate, TicketUpdate, TicketResponse
from typing import List
from typing import Dict

router = APIRouter()

# In-memory storage for tickets
tickets_db: Dict[str, TicketSO] = {}

#  POST localhost.com/tickets  {data: TicketCreate}
@router.post("/", response_model=TicketResponse)
def create(data: TicketCreate):
    print("create logs------------------")
    return crud.create_ticket(data)

#  GET localhost.com/tickets {}
@router.get("/", response_model=List[TicketResponse])
def list_tickets():
    print("logs------------------")
    return crud.get_all_tickets()

#  GET localhost.com/tickets {ticket_id}
@router.get("/{ticket_id}", response_model=TicketResponse)
def read(ticket_id: str):
    print("logs------------------")
    ticket = crud.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

#  PUT localhost.com/tickets {ticket_id}
@router.put("/{ticket_id}", response_model=TicketResponse)
def update(ticket_id: str, data: TicketUpdate):
    ticket = crud.update_ticket(ticket_id, data)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

#  DELETE localhost.com/tickets {ticket_id}
@router.delete("/{ticket_id}")
def delete(ticket_id: str):
    result = crud.delete_ticket(ticket_id)
    if not result:
        raise HTTPException(result)
    return {"message": "Ticket deleted"}
