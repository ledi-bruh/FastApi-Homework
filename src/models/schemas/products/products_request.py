from pydantic import BaseModel


class ProductsRequest(BaseModel):
    name: str
