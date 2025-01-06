from fastapi import APIRouter, HTTPException, Request, status
from tortoise.exceptions import DoesNotExist

from use_case.city_service.city_service import CityService
from db.repositories.location_repositories.city_repositories import CityRepository
from db.schemas.location_schema.city_schemas import CityOutSchema, FullCitySchema
from config.components.logging_config import logger


city_router = APIRouter()

@city_router.get("/{city_slug}", response_model=FullCitySchema, status_code=status.HTTP_200_OK)
async def get_city(city_slug: str, request: Request):
    try:
        city = await CityService.get_city_by_slug(city_slug)
        if city is None:
            raise HTTPException(status_code=404, detail="В городе нет салона или мастера")
        return city
    except DoesNotExist:
        logger.error(f"Город с slug {city_slug} не существует.")
        raise HTTPException(status_code=404, detail="Город не существует.")
    except Exception as e:
        logger.error(f"Внутренняя ошибка сервера: {str(e)}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера.")
