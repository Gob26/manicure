from sqlite3 import IntegrityError
from typing import Optional, Dict
from venv import create

from fastapi import HTTPException, status
from markdown_it.common.html_re import attribute
from tortoise.exceptions import DoesNotExist
from db.schemas.service_schemas.service_attribute_schemas import TemplateAttributeResponseSchema
from db.repositories.services_repositories.service_standart_atrribute_repositories import ServiceAttributeTypeRepository, ServiceAttributeValueRepository, TemplateAttributeRepository
from db.models.services_models.service_standart_model import ServiceAttributeType, ServiceAttributeValue, TemplateAttribute 


from db.schemas.service_schemas.service_attribute_schemas import ServiceAttributeTypeCreateSchema, \
    ServiceAttributeTypeResponseSchema, TemplateAttributeCreateSchema
from use_case.utils.slug_generator import generate_unique_slug
from config.components.logging_config import logger


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
    
    @staticmethod
    async def delete_attribute_type(id: int) -> None:
        """Удаление типа атрибута"""
        if not await ServiceAttributeTypeRepository.get_or_none_attribute_types_id(id=id):
            raise HTTPException(status_code=404, detail="Тип атрибута неяден.")
        await ServiceAttributeTypeRepository.delete_service_attribute_type(id=id)


# AttributeValue
class ServiceAttributeValueService:

    @staticmethod
    async def get_or_none_attribute_value(slug: str) -> Optional[ServiceAttributeValue]:
        """Получение типа атрибута по slug"""
        try:
            return await ServiceAttributeValueRepository.get_or_none_attribute_value_by_slug(slug=slug)
        except Exception as e:
            logger.error(f"Ошибка при получении типа атрибута: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Ошибка при получении типа атрибута.")

    @staticmethod
    async def create_attribute_value(attribute_type_id: int, name: str, slug: str) -> ServiceAttributeValue:
        """Создание нового типа атрибута"""
        if not slug:
            slug = await generate_unique_slug(ServiceAttributeValue, name)
        attribute_value = await ServiceAttributeValueRepository.create_service_attribute_value(
                attribute_type_id=attribute_type_id, name=name, slug=slug
            )
        return attribute_value

    @staticmethod
    async def get_list_attribute_values(attribute_type_id: int) -> Dict[str, str]:
        """Получение всех значений атрибутов"""
        attribute_values = await ServiceAttributeValueRepository.get_all_attribute_values(attribute_type_id)
        return {str(attr_value.id): attr_value.name for attr_value in attribute_values}

    @staticmethod
    async def get_or_none_attribute_value_id(id: int) -> ServiceAttributeValue:
        attribute_value = await ServiceAttributeValueRepository.get_or_none_attribute_value_id(id)
        return attribute_value

    @staticmethod
    async def delete_attribute_value(id: int) -> None:
        """Удаление типа атрибута"""
        if not await ServiceAttributeValueRepository.get_or_none_attribute_value_id(id=id):
            raise HTTPException(status_code=404, detail="Тип атрибута неяден.")
        await ServiceAttributeValueRepository.delete_service_attribute_value(id=id)

    @staticmethod
    async def update_attribute_value(
        attribute_value: ServiceAttributeValue,
        name: str,
        slug: str,
    ) -> ServiceAttributeValue:
        """
        Обновление типа атрибута.
        """
        return await ServiceAttributeValueRepository.update_service_attribute_value(
            id=attribute_value.id,
            name=name,
            slug=slug,
        )


class TemplateAttributeService:
    @staticmethod
    async def attach_attribute(data: TemplateAttributeCreateSchema):
        """
        Привязывает атрибут к шаблону услуги.
        """
        # Проверяем существование связи
        existing = await TemplateAttributeRepository.get_existing_template_attribute(
            service_template_id=data.service_template_id,
            attribute_type_id=data.attribute_type_id
        )
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Связь атрибута с шаблоном уже существует."
            )

        # Создаем новую связь
        created = await TemplateAttributeRepository.create_template_attribute(data.dict())
        # Преобразуем ORM объект в Pydantic модель с использованием model_validate
        return TemplateAttributeResponseSchema(**created.__dict__)

    @staticmethod
    async def get_list_by_service_template(id: int):
        """
        Получает список атрибутов, привязанных к указанному шаблону услуги.
        """
        attributes = await TemplateAttributeRepository.get_by_service_template(id)
        if not attributes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Атрибуты для указанного шаблона услуги не найдены."
            )
        # Преобразуем каждый ORM-объект в Pydantic-схему
        return [TemplateAttributeResponseSchema(**attribute.__dict__) for attribute in attributes]