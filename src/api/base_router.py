from fastapi import APIRouter
from src.api import users, products, tanks


base_router = APIRouter()
base_router.include_router(users.router)
base_router.include_router(products.router)
base_router.include_router(tanks.router)
