from pydantic import BaseModel
from src.models.base import Base

def create_by(model: Base, schema: BaseModel, current_user: dict) -> Base:
    for field, value in schema:
        setattr(model, field, value)
    setattr(model, 'created_by', current_user.get('id'))
    setattr(model, 'modified_by', current_user.get('id'))
    return model 
