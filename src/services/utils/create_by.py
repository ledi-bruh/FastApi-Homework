from pydantic import BaseModel
from src.models.base import Base

def create_by(model: Base, schema: BaseModel, current_user_id: int) -> Base:
    for field, value in schema:
        setattr(model, field, value)
    setattr(model, 'created_by', current_user_id)
    setattr(model, 'modified_by', current_user_id)
    return model 
