from pydantic import BaseModel


class TanksRequest(BaseModel):
    name: str
    max_capacity: float
    current_capacity: float
    product_id: int
