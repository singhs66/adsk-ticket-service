from uuid import UUID

from pydantic import BaseModel
from typing import Optional


class TicketSO(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: str
    status: Optional[str] = "open"
    severity: Optional[str] = "medium"
