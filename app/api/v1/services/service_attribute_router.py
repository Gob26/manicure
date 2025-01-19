from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, status

from db.models.services_models.service_standart_model import ServiceAttributeType, ServiceAttributeValue, TemplateAttribute 
from app.db.schemas.service_schemas.service_attribute_schemas import ServiceAttributeTypeCreateSchema, \
    ServiceAttributeTypeResponseSchema, ServiceAttributeTypeDictResponseSchema
from app.use_case.service_service.service_standart_attribute_service import ServiceAttributeTypeService, ServiceAttributeValueService, TemplateAttributeService
from use_case.utils.permissions import check_user_permission
from use_case.utils.jwt_handler import get_current_user
from config.components.logging_config import logger


service_attribute_router = APIRouter()


@service_attribute_router.post(
    "/",
    response_model=ServiceAttributeTypeCreateSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_service_attribute_type(
    data: ServiceAttributeTypeCreateSchema,
    current_user: dict = Depends(get_current_user),
):
    # Проверка прав пользователя
    check_user_permission(current_user, ["admin", "master"])

    # Проверяем, существует ли уже тип атрибута с таким slug
    existing = await ServiceAttributeTypeService.get_or_none_attribute_type(slug=data.slug)
    if existing:
        raise HTTPException(status_code=400, detail="Тип атрибута с таким slug уже существует.")

    # Создаем новый тип атрибута
    attribute_type = await ServiceAttributeTypeService.create_attribute_type(**data.dict())
    return attribute_type


@service_attribute_router.get(
    "/all",
    response_model=ServiceAttributeTypeDictResponseSchema,  # Изменена схема ответа
    status_code=status.HTTP_200_OK,
)
async def list_service_attribute_types(
    current_user: dict = Depends(get_current_user),
):
    # Проверка прав пользователя
    check_user_permission(current_user, ["admin", "master", "salon"])

    # Получаем все типы атрибутов
    attribute_types = await ServiceAttributeTypeService.get_list_attribute_types()
    return ServiceAttributeTypeDictResponseSchema(data=attribute_types)