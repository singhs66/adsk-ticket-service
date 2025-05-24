from uuid import UUID

from pydantic import BaseModel, EmailStr
from typing import Optional


# <--------------------------------------------------------->
# API schemas for Ticket Request and Response

class TicketCreate(BaseModel):
    title: str
    description: str
    severity: Optional[str] = "medium"


class TicketUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[str]
    severity: Optional[str]


class TicketResponse(TicketCreate):
    id: UUID
    status: str


# <--------------------------------------------------------->
# API schemas for User Request and Response

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
