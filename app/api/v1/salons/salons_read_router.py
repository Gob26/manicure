from fastapi import APIRouter, HTTPException, status

from core.exceptions.http import NotFoundException, BadRequestException
from core.exceptions.service import ResourceNotFoundException, BusinessRuleException
from db.schemas.salon_schemas.salon_schemas import SalonDetailsSchema
from config.components.logging_config import logger
from use_case.salon_service.salon_read_service import SalonReadService

salon_detail_by_slug_router = APIRouter()


@salon_detail_by_slug_router.get(
    "/{salon_slug}",
    response_model=SalonDetailsSchema,
    summary="Получение полной инфорамации о салоне",
    description="Получить информацию о салоне по слагу"
)
async def get_salon_by_slug(salon_slug: str):
    """Эндпоинт для получения информации о салоне по slug"""
    try:
        # API слой больше не проверяет наличие салона - это теперь делает сервисный слой
        return await SalonReadService.get_salon_by_slug(salon_slug)
    except ResourceNotFoundException as e:
        # Преобразуем ошибку сервисного слоя в HTTP ошибку
        raise NotFoundException(message=e.message, error_code=e.error_code)
    except BusinessRuleException as e:
        raise BadRequestException(message=e.message, error_code=e.error_code)
    except Exception as e:
        logger.error(f"Непредвиденная ошибка при получении салона: {e}", exc_info=True)
        # В идеале здесь должен быть свой код ошибки из error_codes.py
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Системная ошибка при получении информации о салоне"
        )