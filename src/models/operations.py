from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from src.models.base import Base


class Operations(Base):
    __tablename__ = 'operations'
    id = Column(Integer, primary_key=True)
    mass = Column(Float, nullable=False)
    date_start = Column(DateTime(timezone=True), nullable=False)
    date_end = Column(DateTime(timezone=True), nullable=False)
    tank_id = Column(Integer, ForeignKey('tanks.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    modified_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified_by = Column(Integer, ForeignKey('users.id'), nullable=False)
