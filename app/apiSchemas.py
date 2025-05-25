from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, constr
from typing import Optional


# <--------------------------------------------------------->
# API schemas for Ticket Request and Response
class TicketCreate(BaseModel):
    title: constr(max_length=100, strip_whitespace=True)
    description: constr(max_length=255, strip_whitespace=True)
    severity: Optional[str]
    category: Optional[str]
    status: Optional[str] = "Open"

class TicketUpdate(BaseModel):
    description: Optional[constr(max_length=255, strip_whitespace=True)]
    status: Optional[constr(strip_whitespace=True, to_lower=True)]

class TicketResponse(TicketCreate):
    id: UUID
    status: str
    category: Optional[str]
    created_at: datetime
    assignee: Optional[str]


# <--------------------------------------------------------->
# API schemas for User Request and Response
class UserCreate(BaseModel):
    name: constr(min_length=6, max_length=100, strip_whitespace=True)
    email: EmailStr
    password: constr(min_length=8, max_length=100)
