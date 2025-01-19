from typing import Any, Dict
from typing import Optional, List

from fastapi import HTTPException, status
from tortoise.exceptions import DoesNotExist, IntegrityError
from db.models.services_models.service_standart_model import ServiceAttributeType, ServiceAttributeValue, TemplateAttribute 
from db.repositories.base_repositories.base_repositories import BaseRepository
from config.components.logging_config import logger


class ServiceAttributeTypeRepository(BaseRepository):
    model = ServiceAttributeType

    @classmethod
    async def create_service_attribute_type(cls, name: str, slug: str) -> ServiceAttributeType:
        """Создание нового типа атрибута"""
        try:
            return await cls.create(name=name, slug=slug)
        except IntegrityError as e:
            logger.error(f"Ошибка при создании ServiceAttributeType: {str(e)}", exc_info=True)
            raise HTTPException(status_code=400, detail="Тип атрибута с таким slug уже существует.")

    @classmethod
    async def get_service_attribute_type_by_slug(cls, slug: str) -> Optional[ServiceAttributeType]:
        """Получение типа атрибута по slug"""
        return await cls.get_or_none(slug=slug)






class ServiceAttributeValueRepository(BaseRepository):
    model = ServiceAttributeValue





class TemplateAttributeRepository(BaseRepository):
    model = TemplateAttribute


