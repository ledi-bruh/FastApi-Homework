from pydantic import BaseModel


class UsersResponse(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True
