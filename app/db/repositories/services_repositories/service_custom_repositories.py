from typing import Any, Dict, Optional
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
        """Создание нового объекта"""
        try:
            custom_service = await cls.create(**kwargs)
            logger.info(f"Пользовательская услуга создана: {custom_service.id}")
            return custom_service
        except IntegrityError as e:  # Например, нарушение уникальных ограничений
            logger.error(f"Ошибка при создании услуги из-за нарушения целостности данных: {e}")
            raise HTTPException(status_code=400, detail="Ошибка в данных при создании услуги")
        except Exception as e:
            logger.error(f"Ошибка при создании пользовательской услуги: {e}")
            raise HTTPException(status_code=500, detail="Ошибка при создании услуги")
        
    @classmethod
    async def update_service(cls, service_id: int, update_data: Dict[str, Any]) -> CustomService:
        """Обновление пользовательской услуги"""
        try:
            service = await cls.get_or_none(id=service_id)
            if not service:
                raise HTTPException(status_code=404, detail="Услуга не найдена")

            await service.update_from_dict(update_data).save()
            logger.info(f"Услуга с ID {service_id} обновлена.")
            return service
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Услуга не найдена")
        except Exception as e:
            logger.error(f"Ошибка при обновлении услуги {service_id}: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Ошибка при обновлении услуги")        

    @classmethod
    async def add_photos_to_custom_service(cls, custom_service_id: int, photo_id: int):
        """Добавление фото к пользовательской услуге"""
        try:
            service = await cls.get_custom_service_by_id(id=custom_service_id)
            
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

    @classmethod
    async def get_custom_service_by_id(cls, id: int) -> Optional[CustomService]:  # Важно указать Optional
        """Получение услуги по ее ID. Возвращает None, если услуга не найдена."""
        try:
            custom_service = await cls.get_or_none(id=id)
            return custom_service  # Просто возвращаем None, если не найдено
        except Exception as e:
            logger.error(f"Произошла ошибка при получении услуги: {e}",
                         exc_info=True)  # Добавил exc_info=True для более подробного логирования
            raise  # Перебрасываем исключение, чтобы обработать его выше (например, в сервисе или обработчике ошибок)

    