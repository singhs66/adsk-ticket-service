from pydantic import BaseModel
from typing import Optional


class TicketSO(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    status: Optional[str] = "open"
    priority: Optional[str] = "medium"
