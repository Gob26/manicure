from typing import List
from fastapi import APIRouter, HTTPException, status
from use_case.master_service.master_read_service import MasterListService
from db.schemas.master_schemas.master_schemas import MasterListSchema
from config.components.logging_config import logger

master_list_router = APIRouter()


@master_list_router.get(
    "/{city_slug}/masters",
    response_model=List[MasterListSchema],
    summary="Получение списка мастеров города"
    description="Получить список мастеров города"
)
async def get_masters_by_city(city_slug: str):
    """
    Получение списка мастеров для города по slug
    """
    logger.info(f"Запрос на получение мастеров для города с slug: {city_slug}")

    try:
        masters = await MasterListService.get_masters_by_city(city_slug)

        if not masters:
            logger.warning(f"Мастера для города '{city_slug}' не найдены.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Мастера для города '{city_slug}' не найдены."
            )

        logger.info(f"Найдено {len(masters)} мастеров для города '{city_slug}'.")
        return masters

    except Exception as e:
        logger.error(f"Ошибка при получении мастеров для города '{city_slug}': {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обработке запроса. Попробуйте позже."
        )
