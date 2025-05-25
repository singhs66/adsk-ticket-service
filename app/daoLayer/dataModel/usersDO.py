from sqlalchemy import Column, String, Text, DateTime, func, INT, Boolean, Integer
from app.daoLayer.database_base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, nullable=False,  primary_key=True, unique=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255))
    phone_number = Column(Integer)
    address = Column(Text)
    department = Column(String(255))
    active = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    password = Column(String(255), nullable=False)
