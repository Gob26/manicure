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


@service_attribute_router.get(
    "/{attribute_type_id}",
    response_model=ServiceAttributeTypeResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_service_attribute_type(
    attribute_type_id: int,
    current_user: dict = Depends(get_current_user),
):
    # Проверка прав пользователя
    check_user_permission(current_user, ["admin", "master", "salon"])

    # Получаем тип атрибута по id
    attribute_type = await ServiceAttributeTypeService.get_or_none_attribute_type(id=attribute_type_id)
    if not attribute_type:
        raise HTTPException(status_code=404, detail="Тип атрибута не найден.")
    return attribute_type


#обновление атрибута
@service_attribute_router.put(
    "/{attribute_type_id}",
    response_model=ServiceAttributeTypeCreateSchema,
    status_code=status.HTTP_200_OK,
)
async def update_service_attribute_type(
    attribute_type_id: int,
    data: ServiceAttributeTypeCreateSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Обновление типа атрибута услуги.
    """
    # Проверка прав текущего пользователя
    check_user_permission(current_user, ["admin", "master"])

    # Получение текущего атрибута по его ID
    attribute_type = await ServiceAttributeTypeService.get_or_none_attribute_type_by_id(attribute_type_id)
    if not attribute_type:
        raise HTTPException(status_code=404, detail="Тип атрибута не найден.")

    # Обновление атрибута через сервис
    updated_attribute_type = await ServiceAttributeTypeService.update_attribute_type(
        attribute_type=attribute_type,
        name=data.name,
        slug=data.slug,
    )

    if not updated_attribute_type:
        raise HTTPException(status_code=500, detail="Не удалось обновить тип атрибута.")

    return updated_attribute_type