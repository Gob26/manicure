from typing import List
from fastapi import APIRouter, HTTPException, Request, status
from tortoise.exceptions import DoesNotExist

from use_case.city_service.city_service import CityService
from db.schemas.location_schema.city_schemas import FullCitySchema, CityLinkSchema
from config.components.logging_config import logger


city_router = APIRouter()

@city_router.get("/{city_slug}",
                 response_model=FullCitySchema,
                 status_code=status.HTTP_200_OK,
                 summary="Получение города по slug",
                 description="Получить город по его слагу"
                 )
async def get_city(city_slug: str, request: Request):
    try:
        city = await CityService.get_city_by_slug(city_slug)
        return city
    except HTTPException as http_ex:
        logger.error(f"Ошибка при получении города {city_slug}: {str(http_ex)}")
        raise http_ex
    except DoesNotExist:
        logger.error(f"Город с slug {city_slug} не существует")
        raise HTTPException(status_code=404, detail="Город не найден")
    except Exception as e:
        logger.error(f"Внутренняя ошибка сервера при получении города {city_slug}: {str(e)}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@city_router.get(
    "/",
    response_model=List[CityLinkSchema],
    status_code=status.HTTP_200_OK,
    summary="Список городов в которых есть салон или мастер",
    description="Получить список городов с активными салонами или мастерами"
)
async def get_active_cities():
    try:
        cities = await CityService.get_active_cities()
        return cities
    except Exception as e:
        logger.error(f"Ошибка при получении списка активных городов: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервера при получении списка городов"
        )
