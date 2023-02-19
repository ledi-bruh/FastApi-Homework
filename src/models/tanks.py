from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.models.base import Base


class Tanks(Base):
    __tablename__ = 'tanks'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    max_capacity = Column(Float, nullable=False)
    current_capacity = Column(Float, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    modified_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    product = relationship('Products', backref='tank_product')
