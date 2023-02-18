from pydantic import BaseModel
from datetime import datetime


class ProductsResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    created_by: int
    modified_at: datetime
    modified_by: int

    class Config:
        orm_mode = True
