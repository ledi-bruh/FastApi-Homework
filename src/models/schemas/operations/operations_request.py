from pydantic import BaseModel
from datetime import datetime


class OperationsRequest(BaseModel):
    mass: float
    date_start: datetime
    date_end: datetime
    tank_id: int
    product_id: int
