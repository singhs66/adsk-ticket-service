from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, constr
from typing import Optional

class TicketSO(BaseModel):
    id: Optional[UUID] = None
    title: constr(min_length=1, max_length=100, strip_whitespace=True)
    description: constr(min_length=1, max_length=255, strip_whitespace=True)
    status: constr(strip_whitespace=True, to_lower=True)
    severity: Optional[str]
    category: Optional[str]
    assignee: Optional[str] = None
    created_at: datetime
