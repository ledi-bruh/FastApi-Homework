from fastapi import FastAPI
from api.base_router import base_router


app = FastAPI(
    title='Приложение FastAPI',
    description='Без комментариев :D',
    version='0.0.1',
)

app.include_router(base_router)
