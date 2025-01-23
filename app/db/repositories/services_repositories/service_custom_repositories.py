from typing import Any, Dict
from fastapi import HTTPException, status
from tortoise.exceptions import DoesNotExist, IntegrityError

from db.models.services_models.service_custom_model import CustomService
from db.repositories.base_repositories.base_repositories import BaseRepository
from db.models.photo_models.photo_standart_service_model import CustomServicePhoto
from config.components.logging_config import logger


class ServiceCustomRepository(BaseRepository):
    model = CustomService

    @classmethod
    async def create_custom_service(cls, **kwargs) -> CustomService:
        try:
            custom_service = await cls.create(**kwargs)
            logger.info(f"Пользовательская услуга создана: {custom_service.id}")
            return custom_service
        except Exception as e:
            logger.error(f"Ошибка при создании пользовательской услуги: {e}")
            raise HTTPException(status_code=500, detail="Ошибка при создании услуги")
        
    @classmethod
    async def add_photos_to_service(cls, custom_service_id: int, photo_id: int) -> CustomServicePhoto:
        """Добавление фотографии к пользовательской услуге."""
        try:
            service_photo = await CustomServicePhoto.create(
                service_id=custom_service_id,
                photo_id=photo_id
            )
            logger.info(f"Фото {photo_id} связано с пользовательской услугой {custom_service_id}")
            return service_photo
        except Exception as e:
            logger.error(f"Ошибка при добавлении фото к услуге: {e}")
            raise HTTPException(status_code=500, detail="Ошибка при связывании фото с услугой")