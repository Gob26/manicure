# Проверьте файл с маршрутами (например, cities_router.py)
from fastapi import APIRouter

router = APIRouter()

@router.get("/cities", status_code=200)
async def get_cities():
    # логика получения городов
    pass

# Затем убедитесь, что роутер импортирован и подключен в main.py или __init__.py
from fastapi import FastAPI
from .routes.cities_router import router as cities_router

app = FastAPI()

app.include_router(cities_router, prefix="/api/v1", tags=["cities"])