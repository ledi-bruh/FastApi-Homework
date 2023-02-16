from datetime import datetime, timezone
from src.models.base import Base


def modified_by_now(model: Base, current_user: dict) -> None:
    print(current_user)
    setattr(model, 'modified_at', datetime.now(timezone.utc))
    setattr(model, 'modified_by', current_user.get('id'))
