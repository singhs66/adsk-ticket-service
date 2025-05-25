from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from typing import Optional


class TicketSO(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: str
    status: Optional[str] = "Open"
    severity: Optional[str]
    category: Optional[str]
    assignee: Optional[str] = None
    created_at: datetime
