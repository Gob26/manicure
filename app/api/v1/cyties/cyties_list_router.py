from typing import List

from fastapi import APIRouter, HTTPException, status
from core.redis import get_redis_client
from use_case.city_service.cities_list_service import CityListService
from db.schemas.location_schema.city_schemas import FullCitySchema, CityOutAllSchema
from config.components.logging_config import logger

# Инициализация маршрута
cities_list_router = APIRouter()

# Получаем Redis клиент
redis_client = get_redis_client()

# Создаем экземпляр сервиса с передачей клиента Redis для кеширования
city_service = CityListService(cache=redis_client)


@cities_list_router.get(
    "/",
    response_model=List[FullCitySchema],
    status_code=status.HTTP_200_OK,
    summary="Список городов с полной информацией",
    description="Получить полный список городов со всеми данными с активными салонами или мастерами"
)
async def get_active_cities():
    """
    Эндпоинт для получения списка городов.
    Попытка сначала получить данные из кеша, если их нет - загружаем из базы данных.
    """
    try:
        logger.info("Запрос списка активных городов")

        # Получаем активные города с кешированием
        cities = await city_service.get_active_cities_list()

        logger.info(f"Получено {len(cities)} городов")
        return cities
    except Exception as e:
        # Логируем ошибку, если она возникла
        logger.error(f"Ошибка при получении списка активных городов: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера при получении списка городов"
        )


@cities_list_router.get(
    "/all",
    response_model=List[CityOutAllSchema],
    status_code=status.HTTP_200_OK,
    summary="Список всех городов",
    description="Получеие всех городов из базы для выбора при регистрации"
)
async def get_all_cities():
    """
    Эндпоинт для получения списка всех городов.
    Попытка сначала получить данные из кеша, если их нет - загружаем из базы данных.
    """
    try:
        logger.info("Запрос списка всех городов")

        # Получение всех городов с кешированием
        cities = await city_service.get_all_cities_list()

        logger.info(f"Получено {len(cities)} городов")
        return cities
    except Exception as e:
        # Логируем ошибку, если возникает
        logger.error(f"Ошибка при получении списка всех городов: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера при получении списка городов"
    )