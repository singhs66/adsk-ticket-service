from pydantic import BaseModel
from typing import Optional


class TicketCreate(BaseModel):
    title: str
    description: str
    priority: Optional[str] = "medium"


class TicketUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[str]
    priority: Optional[str]


class TicketResponse(TicketCreate):
    id: str
    status: str
