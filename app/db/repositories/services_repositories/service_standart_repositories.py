from typing import Any, Dict, Optional, List
from fastapi import HTTPException, status
from tortoise.exceptions import DoesNotExist, IntegrityError
from app.db.schemas.salon_schemas.salon_schemas import SalonUpdateSchema
from db.models.services_models.service_standart_model import StandardService
from db.repositories.base_repositories.base_repositories import BaseRepository
from config.components.logging_config import logger
from db.models.photo_models.photo_standart_service_model import StandardServicePhoto
from db.models import Category
from db.schemas.service_schemas.service_standart_schemas import StandardServiceUpdate


class ServiceStandartRepository(BaseRepository):
    model = StandardService

    @classmethod
    async def create_service_standart(cls, **kwargs) -> StandardService:
        """Создает стандартную услугу."""
        logger.info(f"Создание стандартной услуги с параметрами: {kwargs}")
        try:
            service = await cls.create(**kwargs)
            logger.info(f"Услуга успешно создана с ID: {service.id}")
            return service
        except IntegrityError as e:
            logger.error(f"Ошибка целостности данных: {str(e)}", exc_info=True)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка целостности данных. Проверьте входные данные.")
        except Exception as e:
            logger.error(f"Непредвиденная ошибка: {str(e)}", exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Произошла ошибка при создании услуги.")

    @classmethod
    async def get_service_by_id(cls, service_id: int) -> Optional[StandardService]:
        """Получает услугу по ID или None."""
        try:
            service = await cls.get_or_none(id=service_id)
            if not service:
                logger.warning(f"Услуга с ID {service_id} не найдена.")
            return service
        except Exception as e:
            logger.error(f"Ошибка получения услуги: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при получении услуги.")

    @classmethod
    async def get_category_by_id(cls, category_id: int) -> Optional[Category]:
        """Получает категорию по ID или None."""
        try:
            category = await Category.get_or_none(id=category_id)
            if not category:
                logger.warning(f"Категория с ID {category_id} не найдена.")
            return category
        except Exception as e:
            logger.error(f"Ошибка получения категории: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при получении категории.")

    @classmethod
    async def link_photo_to_service(cls, service_id: int, photo_id: int) -> None:
        """Привязывает фото к услуге."""
        try:
            service = await cls.get_service_by_id(service_id)
            if not service:
                raise HTTPException(status_code=404, detail=f"Сервис с ID {service_id} не найден.")

            photo = await StandardServicePhoto.get_or_none(id=photo_id)
            if not photo:
                raise HTTPException(status_code=404, detail=f"Фото с ID {photo_id} не найдено.")

            service.default_photo = photo
            await service.save()
            logger.info(f"Фото с ID: {photo_id} успешно привязано к сервису ID: {service_id}")
        except HTTPException as he:
            raise he # Пробрасываем HTTP исключения
        except Exception as e:
            logger.error(f"Ошибка при привязке фото: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Ошибка при привязке фото к сервису.")


    @classmethod
    async def update_service(cls, service_id: int, schema: StandardServiceUpdate) -> StandardService:
        """Обновление стандартной услуги"""
        update_data = {
            k: v for k, v in schema.dict(exclude_unset=True).items()
            if v is not None
        }

        await cls.update(service_id, **update_data)  # Выполняем обновление в БД
        updated_service = await cls.get_by_id(service_id)  # Получаем обновленную услугу из БД

        if updated_service is None:
            raise ValueError(f"Услуга с ID {service_id} не найдена")

        return updated_service