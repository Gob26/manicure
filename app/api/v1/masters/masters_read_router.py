from fastapi import APIRouter, HTTPException, status
from use_case.master_service.master_read_service import MasterReadService
from db.schemas.master_schemas.master_schemas import  MasterDetailSchema
from config.components.logging_config import logger
from app.core.exceptions.service import ResourceNotFoundException
master_read_router = APIRouter()


# Получение мастера по slug
@master_read_router.get(
    "/{city_slug}/masters/{master_slug}",
    response_model=MasterDetailSchema,
    summary="Получение мастера по slug города и slug мастера",
    description="Получение мастера по slug города и slug мастера"
)
async def get_master_by_city_and_slug_route(city_slug: str, master_slug: str):
    """
    Получение мастера по slug города и slug мастера.
    """
    # Логируем начало запроса
    logger.info(f"Запрос на получение мастера: Город - {city_slug}, Мастер - {master_slug}")

    try:
        # Пытаемся получить мастера через сервис
        master = await MasterReadService.get_master(city_slug, master_slug)
        # Логируем успешный результат
        logger.info(f"Мастер {master_slug} найден в городе {city_slug}.")
        return master


    except ResourceNotFoundException as e: # Явно перехватываем ResourceNotFoundException
        logger.error(f"Мастер '{master_slug}' в городе '{city_slug}' не найден: {e}") # Логируем ошибку ResourceNotFoundException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, # Возвращаем 404 Not Found
            detail=f"Мастер с slug {master_slug} в городе {city_slug} не найден."
        )

    except Exception as e: # Обработка всех остальных исключений (ServiceException, ValidationException и т.д.)
        # Логируем любые другие исключения
        logger.error(f"Произошла ошибка при получении мастера: {str(e)}", exc_info=True) # Добавили exc_info=True для трассировки
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении данных о мастере."
        )

