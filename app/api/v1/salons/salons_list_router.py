from typing import List
from fastapi import APIRouter, HTTPException, status
from use_case.salon_service.salon_read_service import SalonListService
from db.schemas.salon_schemas.salon_schemas import SalonListSchema
from config.components.logging_config import logger

salons_list_router = APIRouter()


@salons_list_router.get(
    "/{city_slug}/salons",
    response_model=List[SalonListSchema],
    summary="Получение салонов города",
    description="Получить салоны определенного города по слагу"
)
async def get_salon_by_city_slug(city_slug: str):
    """
    Получение списка мастеров для города по slug
    """
    try:
        salon_service = SalonListService()  # Создаем экземпляр, если метод не @classmethod
        salons = await salon_service.get_salon_by_city(city_slug)

        if not salons:  # Исправленный вариант проверки на пустой список
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Салоны в данном городе не найдены"
            )

        return salons

    except Exception as e:
        logger.error(f"Ошибка при получении списка салонов: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка сервера при получении списка салонов"
        )
