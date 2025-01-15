from typing import Any, Dict
from fastapi import HTTPException, status
from tortoise.exceptions import DoesNotExist, IntegrityError
from db.models.services_models.service_standart_model import StandardService
from db.repositories.base_repositories.base_repositories import BaseRepository
from config.components.logging_config import logger
from db.models.photo_models.photo_standart_service_model import StandardServicePhoto


class ServiceStandartRepository(BaseRepository):
    model = StandardService

    @classmethod
    async def create_service_standart(cls, **kwargs) -> StandardService:
        """
        Создает стандартную услугу, проверяя наличие связанных объектов, таких как фотографии.
        """
        logger.info(f"Создание стандартной услуги с параметрами: {kwargs}")

        try:
            # Проверка существования фото, если указан default_photo_id
            default_photo_id = kwargs.get("default_photo_id")
            if default_photo_id:
                await cls._check_photo_existence(default_photo_id)

            # Создаем услугу
            service = await cls.create(**kwargs)
            logger.info(f"Услуга успешно создана с ID: {service.id}")
            return service

        except IntegrityError as e:
            logger.error(f"Ошибка целостности данных: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ошибка целостности данных. Проверьте входные данные."
            )
        except HTTPException as he:
            logger.error(f"HTTP ошибка при создании услуги: {he.detail}", exc_info=True)
            raise he
        except Exception as e:
            logger.error(f"Непредвиденная ошибка: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла ошибка при создании услуги."
            )

    @staticmethod
    async def _check_photo_existence(photo_id: int) -> None:
        """
        Проверяет, существует ли фото с указанным ID.
        """
        try:
            photo = await StandardServicePhoto.get(id=photo_id)
            logger.info(f"Фото с ID {photo_id} успешно найдено: {photo}")
        except DoesNotExist:
            logger.error(f"Фото с ID {photo_id} не найдено в таблице standard_service_photos")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Фото с ID {photo_id} не найдено."
            )
