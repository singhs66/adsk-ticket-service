from fastapi import APIRouter, HTTPException
from app import crud
from app.daoLayer.serviceObjects.TicketSO import TicketSO
from app.apiSchemas import TicketCreate, TicketUpdate, TicketResponse
from typing import List
from typing import Dict

router = APIRouter()

# In-memory storage for tickets
tickets_db: Dict[str, TicketSO] = {}


@router.post("/", response_model=TicketResponse)
def create(data: TicketCreate):
    print("create logs------------------")
    return crud.create_ticket(data)


@router.get("/", response_model=List[TicketResponse])
def list_tickets():
    print("logs------------------")
    return crud.get_all_tickets()


@router.get("/{ticket_id}", response_model=TicketResponse)
def read(ticket_id: str):
    print("logs------------------")
    ticket = crud.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.put("/{ticket_id}", response_model=TicketResponse)
def update(ticket_id: str, data: TicketUpdate):
    ticket = crud.update_ticket(ticket_id, data)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.delete("/{ticket_id}")
def delete(ticket_id: str):
    result = crud.delete_ticket(ticket_id)
    if not result:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"message": "Ticket deleted"}
