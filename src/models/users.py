from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from src.models.base import Base


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password_hashed = Column(String, nullable=False)
    role = Column(String(length=6), server_default='viewer', nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    modified_at = Column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.current_timestamp(), nullable=False)
    modified_by = Column(Integer, ForeignKey('users.id'), nullable=True)

# ? server_onupdate не работает
