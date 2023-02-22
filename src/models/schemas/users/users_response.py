from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UsersResponse(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime
    created_by: Optional[int]
    modified_at: datetime
    modified_by: Optional[int]

    class Config:
        orm_mode = True
