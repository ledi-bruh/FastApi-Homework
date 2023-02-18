from pydantic import BaseModel
from datetime import datetime


class TanksResponse(BaseModel):
    id: int
    name: str
    max_capacity: float
    current_capacity: float
    product_id: int
    created_at: datetime
    created_by: int
    modified_at: datetime
    modified_by: int
    

    class Config:
        orm_mode = True
