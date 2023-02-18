from datetime import datetime, timezone
from pydantic import BaseModel
from src.models.base import Base


# ! мб в UsersService ?
def modify_by_now(model: Base, schema: BaseModel, current_user: dict) -> None:
    for field, value in schema:
        setattr(model, field, value)
    setattr(model, 'modified_at', datetime.now(timezone.utc))
    setattr(model, 'modified_by', current_user.get('id'))
