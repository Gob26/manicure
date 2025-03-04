from config.components.logging_config import logger
from db.repositories.salon_repositories.salon_repositories import SalonRepository
from core.exceptions.service import ResourceNotFoundException, BusinessRuleException, ServiceException
from core.exceptions.validation import ValidationException
from core.exceptions.repository import EntityNotFoundException


class SalonReadService:
    @staticmethod
    async def get_salon_by_slug(slug: str):
        try:
            # Базовая валидация
            if not slug or not isinstance(slug, str):
                raise ValidationException(message="Недопустимый slug")

            return await SalonRepository.get_salon_by_slug(slug)


        except EntityNotFoundException as e:
            # Преобразуем ошибку репозитория в ошибку сервисного слоя
            raise ResourceNotFoundException(
                resource_type="Салон",
                identifier=slug,
                error_code="SALON_NOT_FOUND"
            )
        except ValidationException:
            # Просто пробрасываем дальше
            raise
        except Exception as e:
            # Логируем и преобразуем в ServiceException
            logger.error(f"Ошибка сервиса при получении салона по slug '{slug}': {e}")
            raise ServiceException(
                message=f"Ошибка при получении данных салона",
                error_code="SERVICE_ERROR"
            )