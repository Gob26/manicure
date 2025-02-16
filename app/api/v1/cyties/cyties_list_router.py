from typing import List, Optional
from fastapi import APIRouter, HTTPException, Request, status
from tortoise.exceptions import DoesNotExist

from db.schemas.location_schema.city_schemas import FullCitySchema
from config.components.logging_config import logger
from use_case.city_service.cities_list_service import CityListService

cities_list_router = APIRouter()

@cities_list_router.get(
    "/",
    response_model=List[FullCitySchema],
    status_code=status.HTTP_200_OK,
    summary="Список городов c полной информацией",
    description="Получить полный список городов со ВСЕМИ данными с активными салонами или мастерами"
)
async def get_active_cities():
    try:
        cities = await CityListService.get_active_cities_list()
        return cities
    except Exception as e:
        logger.error(f"Ошибка при получении списка активных городов: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервера при получении списка городов"
        )