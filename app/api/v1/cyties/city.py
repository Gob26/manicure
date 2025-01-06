from fastapi import APIRouter, HTTPException, status
from tortoise.exceptions import DoesNotExist

from db.repositories.location_repositories.city_repositories import CityRepository
from db.schemas.location_schema.city_schemas import CityOutSchema, FullCitySchema
from config.components.logging_config import logger

#отображение всей информации о городе

city_router = APIRouter()

@city_router.get("/{city_slug}", response_model=FullCitySchema, status_code=status.HTTP_200_OK)
async def get_city(city_slug: str):
    # Вызываем сервис для проверки наличия мастеров или салонов
    city = await city_service.get_city_if_exists(city_slug)
    if city is None:
        raise HTTPException(status_code=404, detail="Город не найден. Так как в нем нет салонов или мастеров.")
    return city
