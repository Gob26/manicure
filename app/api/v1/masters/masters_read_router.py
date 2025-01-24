from fastapi import APIRouter, HTTPException, status
from use_case.master_service.master_read_service import MasterReadService
from db.schemas.master_schemas.master_schemas import MasterCreateSchema
from config.components.logging_config import logger

master_read_router = APIRouter()


# Получение мастера по slug
@master_read_router.get(
    "/{city_slug}/masters/{master_slug}",
    response_model=MasterCreateSchema,
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

        # Если мастер не найден, выбрасываем ошибку
        if not master:
            logger.error(f"Мастер с slug {master_slug} в городе {city_slug} не найден.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Мастер с slug {master_slug} в городе {city_slug} не найден."
            )

        # Логируем успешный результат
        logger.info(f"Мастер {master_slug} найден в городе {city_slug}.")
        return master

    except Exception as e:
        # Логируем любые другие исключения
        logger.error(f"Произошла ошибка при получении мастера: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении данных о мастере."
        )
