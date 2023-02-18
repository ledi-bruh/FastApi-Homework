from pydantic import BaseModel
from datetime import datetime


class UsersResponse(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime
    created_by: int = None
    modified_at: datetime
    modified_by: int = None

    class Config:
        orm_mode = True
