from fastapi import FastAPI
from src.api.base_router import base_router
from src.utils.admin_exist import admin_exist


app = FastAPI(
    title='Приложение FastAPI',
    description='ДЗ',
    version='0.0.1',
    on_startup=[admin_exist],
)

app.include_router(base_router)
