from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr
from typing import Optional


# <--------------------------------------------------------->
# API schemas for Ticket Request and Response

class TicketCreate(BaseModel):
    title: str
    description: str
    severity: Optional[str] = "medium"
    category: Optional[str] = "other"


class TicketUpdate(BaseModel):
    description: Optional[str]
    status: Optional[str]

class TicketResponse(TicketCreate):
    id: UUID
    status: str
    category: Optional[str]
    created_at: datetime
    assignee: Optional[str]


# <--------------------------------------------------------->
# API schemas for User Request and Response

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
