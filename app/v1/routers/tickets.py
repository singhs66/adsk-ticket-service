from fastapi import APIRouter, HTTPException, Query, Depends
from app import crud
from app.apiSchemas import TicketCreate, TicketUpdate, TicketResponse
from typing import List
from fastapi.security import OAuth2PasswordBearer
from app.auth.jwt import verify_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/", response_model=TicketResponse)
def create(data: TicketCreate, token_data: dict = Depends(verify_token)):
    print("Authenticated user payload:", token_data)
    print("Creating a new ticket")
    return crud.create_ticket(data)

@router.get("/", response_model=List[TicketResponse])
def list_tickets(status: str = Query(default=None),
                 sort_by: str = Query("created_at"),
                 assignee: str = Query(default=None),
                 token_data: dict = Depends(verify_token)):
    print("Authenticated user payload:", token_data)
    print("Listing all existing ticket")
    return crud.get_all_tickets(status, sort_by, assignee)


@router.get("/{ticket_id}", response_model=TicketResponse)
def read(ticket_id: str, token_data: dict = Depends(verify_token)):
    print("Authenticated user payload:", token_data)
    ticket = crud.get_ticket(ticket_id)
    print("Get ticket successfully:", ticket)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.put("/{ticket_id}", response_model=TicketResponse)
def update(ticket_id: str, data: TicketUpdate, token_data: dict = Depends(verify_token)):
    print("Authenticated user payload:", token_data)
    ticket = crud.update_ticket(ticket_id, data)
    print("Updated ticket successfully: ", ticket)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.delete("/{ticket_id}")
def delete(ticket_id: str, token_data: dict = Depends(verify_token)):
    print("Authenticated user payload:", token_data)
    result = crud.delete_ticket(ticket_id)
    print("Deleted ticket successfully: ", result)
    if not result:
        raise HTTPException(result)
    return {"message": "Ticket deleted"}
