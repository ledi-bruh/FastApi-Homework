from fastapi import APIRouter
from src.api import users


base_router = APIRouter()
base_router.include_router(users.router)
