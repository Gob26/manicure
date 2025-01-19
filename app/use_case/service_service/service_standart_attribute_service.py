from typing import Optional, Dict
from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist
from db.repositories.services_repositories.service_standart_atrribute_repositories import ServiceAttributeTypeRepository, ServiceAttributeValueRepository, TemplateAttributeRepository
from db.models.services_models.service_standart_model import ServiceAttributeType, ServiceAttributeValue, TemplateAttribute 

from config.components.logging_config import logger

class ServiceAttributeTypeService:
    @staticmethod
    async def create_attribute_type(name: str, slug: str) -> Dict[str, str]:
        """Создание нового типа атрибута"""
        attribute_type = await ServiceAttributeTypeRepository.create_service_attribute_type(name=name, slug=slug)
        return {"name": attribute_type.name, "slug": attribute_type.slug}

  
    @staticmethod
    async def get_or_none_attribute_type(slug: str) -> Optional[ServiceAttributeType]:
        """Получение типа атрибута по slug"""
        try:
            return await ServiceAttributeTypeRepository.get_service_attribute_type_by_slug(slug=slug)
        except Exception as e:
            logger.error(f"Ошибка при получении типа атрибута: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Ошибка при получении типа атрибута.")




class ServiceAttributeValueService:
    @staticmethod






class TemplateAttributeService:
    @staticmethod    