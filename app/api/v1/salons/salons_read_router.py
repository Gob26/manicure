from fastapi import APIRouter, HTTPException, status
from app.use_case.salon_service.salon_read_list_service import SalonListService
from db.schemas.salon_schemas.salon_schemas import SalonDetailsSchema
from config.components.logging_config import logger

salon_detail_by_slug_router = APIRouter()


@salon_detail_by_slug_router.get(
    "/{salon_slug}",
    response_model=SalonDetailsSchema,
    summary="Получение полной инфорамации о салоне",
    description="Получить информацию о салоне по слагу"
)
async def get_salon_by_slug(salon_slug: str):
    try:
        if salon := await SalonListService.get_salon_by_slug(salon_slug):
            return salon
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Салон не найден")
    except Exception as e:
        logger.error(f"Системная ошибка при получении информации о салоне: {e}")
        raise HTTPException(status_code=500, detail="Системная ошибка при получении информации о салоне")