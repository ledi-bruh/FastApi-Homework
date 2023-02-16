from pydantic import BaseModel


class ProductsResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
