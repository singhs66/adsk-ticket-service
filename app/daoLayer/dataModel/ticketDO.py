import uuid

from sqlalchemy import Column, String, Text, DateTime, func, UUID, Integer, Index
from app.daoLayer.database_base import Base


class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_by = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    severity = Column(String(50), nullable=False)
    status = Column(String(50), default='open')
    comments = Column(String(255), nullable=True)
    category = Column(String(50))
    assignee = Column(String(255))

    __table_args__ = (
        Index("idx_tickets_status", "status"),
        Index("idx_tickets_created_at", "created_at"),
        Index("idx_tickets_id", "id"),
        Index("idx_tickets_assignee", "assignee"),
    )
