from typing import Optional, Dict
from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist
from db.repositories.services_repositories.service_standart_atrribute_repositories import ServiceAttributeTypeRepository, ServiceAttributeValueRepository, TemplateAttributeRepository
from db.models.services_models.service_standart_model import ServiceAttributeType, ServiceAttributeValue, TemplateAttribute 

from config.components.logging_config import logger
from db.schemas.service_schemas.service_attribute_schemas import ServiceAttributeTypeCreateSchema, \
    ServiceAttributeTypeResponseSchema
from use_case.utils.slug_generator import generate_unique_slug


class ServiceAttributeTypeService:
    @staticmethod
    async def create_attribute_type(name: str, slug: str) -> ServiceAttributeType:
        """Создание нового типа атрибута"""
        if not slug:
            slug = await generate_unique_slug(ServiceAttributeType, name)
        attribute_type = await ServiceAttributeTypeRepository.create_service_attribute_type(name=name, slug=slug)
        return attribute_type

    @staticmethod
    async def get_or_none_attribute_type_by_id(id: int) -> Optional[ServiceAttributeType]:
        """Получение типа атрибута по id"""
        return await ServiceAttributeTypeRepository.get_or_none_attribute_types_id(id=id)
  
    @staticmethod
    async def get_or_none_attribute_type(slug: str) -> Optional[ServiceAttributeType]:
        """Получение типа атрибута по slug"""
        try:
            return await ServiceAttributeTypeRepository.get_service_attribute_type_by_slug(slug=slug)
        except Exception as e:
            logger.error(f"Ошибка при получении типа атрибута: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Ошибка при получении типа атрибута.")

    @staticmethod
    async def get_list_attribute_types() -> Dict[str, str]:
        """Получение всех типов атрибутов"""
        attribute_types = await ServiceAttributeTypeRepository.get_all_attribute_types()
        return {attr_type.slug: attr_type.name for attr_type in attribute_types}

    @staticmethod
    async def update_attribute_type(
        attribute_type: ServiceAttributeType,
        name: str,
        slug: str,
    ) -> ServiceAttributeType:
        """
        Обновление типа атрибута.
        """
        return await ServiceAttributeTypeRepository.update_service_attribute_type(
            id=attribute_type.id,
            name=name,
            slug=slug,
        )



class ServiceAttributeValueService:
    @staticmethod
    async def some_method():
        # Реализация метода
        pass






class TemplateAttributeService:
    @staticmethod
    async def some_method():
        # Реализация метода
        pass