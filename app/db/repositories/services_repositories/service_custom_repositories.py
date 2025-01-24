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
    async def add_photos_to_custom_service(cls, custom_service_id: int, photo_id: int):
        try:
            service = await CustomService.get_or_none(id=custom_service_id)
            if not service:
                raise HTTPException(status_code=404, detail="Услуга не найдена")

            photo = await CustomServicePhoto.get_or_none(id=photo_id)
            if not photo:
                raise HTTPException(status_code=404, detail="Фотография не найдена")

            photo.custom_service = service  # Устанавливаем связь
            await photo.save()

            logger.info(f"Фото {photo_id} связано с пользовательской услугой {custom_service_id}")
            return {"status": "ok"}
        except Exception as e:
            logger.error(f"Неизвестная ошибка: {e}")
            raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
        

    