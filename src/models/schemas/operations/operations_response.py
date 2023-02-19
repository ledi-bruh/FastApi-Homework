from pydantic import BaseModel
from datetime import datetime
from src.models.schemas.tanks.tanks_response import TanksResponse
from src.models.schemas.products.products_response import ProductsResponse


class OperationsResponse(BaseModel):
    id: int
    mass: float
    date_start: datetime
    date_end: datetime
    tank: TanksResponse
    product: ProductsResponse
    created_at: datetime
    created_by: int
    modified_at: datetime
    modified_by: int
    

    class Config:
        orm_mode = True
