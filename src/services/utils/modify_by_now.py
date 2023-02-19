from datetime import datetime, timezone
from src.models.base import Base


# ! мб в UsersService ?
def modify_by_now(model: Base, current_user: dict) -> None:
    setattr(model, 'modified_at', datetime.now(timezone.utc))
    setattr(model, 'modified_by', current_user.get('id'))
