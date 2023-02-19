from pydantic import BaseModel
from datetime import datetime
from src.models.schemas.products.products_response import ProductsResponse


class TanksResponse(BaseModel):
    id: int
    name: str
    max_capacity: float
    current_capacity: float
    product: ProductsResponse
    created_at: datetime
    created_by: int
    modified_at: datetime
    modified_by: int
    

    class Config:
        orm_mode = True
