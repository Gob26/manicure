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

    @classmethod
    async def get_or_none_attribute_types_id(cls, id: int) -> Optional[ServiceAttributeType]:
        """Получение типа атрибута по id"""
        return await cls.get_by_id(id=id)

    @classmethod
    async def get_all_attribute_types(cls) -> List[ServiceAttributeType]:
        """Получение всех типов атрибутов"""
        return await cls.get_all() 

    classmethod
    async def update_service_attribute_type(cls, id: int, name: str, slug: str) -> Optional[ServiceAttributeType]:
        """Обновление типа атрибута"""

        return await cls.update(id=id, name=name, slug=slug)
 


class ServiceAttributeValueRepository(BaseRepository):
    model = ServiceAttributeValue





class TemplateAttributeRepository(BaseRepository):
    model = TemplateAttribute


