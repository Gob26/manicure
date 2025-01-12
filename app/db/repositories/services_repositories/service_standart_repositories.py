from typing import Optional, List, Union, Any
from fastapi import HTTPException, status
from tortoise.exceptions import DoesNotExist
from db.models.services_models.service_standart_model import StandardService
from db.repositories.base_repositories.base_repositories import BaseRepository
from config.components.logging_config import logger


class ServiceStandartRepository(BaseRepository):
    model = StandardService

    @classmethod
    async def create_service_standart(cls, **kwargs: Any) -> StandardService:
            logger.info(f"Начало создание стандартной услуги с параметрами: {kwargs}")
            try:
                service = await cls.create(**kwargs)
                logger.info(f"Категория успешно создана: ID={service.id}")
                return service
            except Exception as e:
                logger.error(f"Ошибка при создании услуги: {e}")
                raise

