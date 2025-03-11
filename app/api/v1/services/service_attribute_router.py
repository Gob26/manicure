from typing import List, Annotated
from fastapi import APIRouter, Depends, File, HTTPException, status, Query

from db.models.services_models.service_standart_model import ServiceAttributeType, ServiceAttributeValue, TemplateAttribute 
from app.db.schemas.service_schemas.service_attribute_schemas import ServiceAttributeTypeCreateSchema, \
    ServiceAttributeTypeResponseSchema, ServiceAttributeTypeDictResponseSchema, ServiceAttributeValueCreateSchema, \
    ServiceAttributeValueDictResponseSchema, ServiceAttributeValueResponseSchema, TemplateAttributeCreateSchema
from app.use_case.service_service.service_standart_attribute_service import ServiceAttributeTypeService, ServiceAttributeValueService, TemplateAttributeService
from use_case.utils.permissions import check_user_permission
from use_case.utils.jwt_handler import get_current_user
from config.components.logging_config import logger


service_attribute_router = APIRouter()

#Эндпоинты для ServiceAttributeType
@service_attribute_router.post(
    "/attribute_types",
    response_model=ServiceAttributeTypeCreateSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создание нового типа атрибута",
    description="Создает новый тип атрибута.",
)
async def create_service_attribute_type(
    data: ServiceAttributeTypeCreateSchema,
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] not in ["admin", "master", "salon"]:
        raise HTTPException(status_code=403, detail="Недостаточно прав для выполнения операции.")

    # Проверяем, существует ли уже тип атрибута с таким slug
    existing = await ServiceAttributeTypeService.get_or_none_attribute_type(slug=data.slug)
    if existing:
        raise HTTPException(status_code=400, detail="Тип атрибута с таким slug уже существует.")

    # Создаем новый тип атрибута
    attribute_type = await ServiceAttributeTypeService.create_attribute_type(**data.dict())
    return attribute_type


@service_attribute_router.get(
    "/list_attribute_types",
    response_model=ServiceAttributeTypeDictResponseSchema,  # Изменена схема ответа
    status_code=status.HTTP_200_OK,
    summary="Получение всех типов атрибутов",
    description="Получает список всех типов атрибутов.",
)
async def list_service_attribute_types(
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] not in ["admin", "master", "salon"]:
        raise HTTPException(status_code=403, detail="Недостаточно прав для выполнения операции.")

    # Получаем все типы атрибутов
    attribute_types = await ServiceAttributeTypeService.get_list_attribute_types()
    return ServiceAttributeTypeDictResponseSchema(data=attribute_types)


@service_attribute_router.get(
    "/{attribute_type_id}",
    response_model=ServiceAttributeTypeResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Получение типа атрибута по ID",
    description="Получает тип атрибута услуги по его ID.",
)
async def get_service_attribute_type(
    attribute_type_id: int,
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] not in ["admin", "master", "salon"]:
        raise HTTPException(status_code=403, detail="Недостаточно прав для выполнения операции.")

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
    summary="Обновление типа атрибута",
    description="Обновляет тип атрибута услуги.",
)
async def update_service_attribute_type(
    attribute_type_id: int,
    data: ServiceAttributeTypeCreateSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Обновление типа атрибута услуги.
    """
    if current_user["role"] not in ["admin", "master", "salon"]:
        raise HTTPException(status_code=403, detail="Недостаточно прав для выполнения операции.")

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

#удаление атрибута 
@service_attribute_router.delete(
    "/{attribute_type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление типа атрибута",
    description="Удаляет тип атрибута услуги.",
)
async def delete_service_attribute_type(
    attribute_type_id: int,
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] not in ["admin", "master", "salon"]:
        raise HTTPException(status_code=403, detail="Недостаточно прав для выполнения операции.")

    # Удаление типа атрибута
    await ServiceAttributeTypeService.delete_attribute_type(attribute_type_id)

    return None

#Эндпоинты для ServiceAttributeValue

@service_attribute_router.post(
    "/attribute_values",
    response_model=ServiceAttributeValueResponseSchema,  
    status_code=status.HTTP_201_CREATED,
    summary="Создание нового значения атрибута",
    description="Создает новое значение атрибута.",
)
async def create_service_attribute_value(
    data: ServiceAttributeValueCreateSchema,
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] not in ["admin", "master", "salon"]:
        raise HTTPException(status_code=403, detail="Недостаточно прав для выполнения операции.")

    # Проверяем, существует ли уже значение атрибута с таким slug
    existing = await ServiceAttributeValueService.get_or_none_attribute_value(slug=data.slug)
    if existing:
        raise HTTPException(status_code=400, detail="Значение атрибута с таким slug уже существует.")

    # Создаем новое значение атрибута
    attribute_value = await ServiceAttributeValueService.create_attribute_value(**data.dict())
    return attribute_value


@service_attribute_router.get(
    "/attribute_values/list_attribute_values/",
    response_model=ServiceAttributeValueDictResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Получение всех значений атрибутов по типу атрибута",
    description="Получение всех значений атрибутов по типу атрибута",
)
async def list_service_attribute_values(
    attribute_type_id: Annotated[int, Query()],  # явно указываем, что это query параметр
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] not in ["admin", "master", "salon"]:
        raise HTTPException(status_code=403, detail="Недостаточно прав для выполнения операции.")

    # Получаем все значения атрибутов для указанного типа
    attribute_values = await ServiceAttributeValueService.get_list_attribute_values(attribute_type_id)
    return ServiceAttributeValueDictResponseSchema(data=attribute_values)

@service_attribute_router.get(
    "attribute_values/{attribute_value_id}",
    response_model=ServiceAttributeValueResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Получить значение атрибута по ID",
    description="Получение значения атрибута по его ID.",
)
async def get_service_attribute_value(
    attribute_value_id: int,
    current_user: dict= Depends(get_current_user),
):
    """
    Возвращает значение атрибута по его ID.
    """
    if current_user["role"] not in ["admin", "master", "salon"]:
        raise HTTPException(status_code=403, detail="Недостаточно прав для выполнения операции.")

    attribute_value = await ServiceAttributeValueService.get_or_none_attribute_value_id(attribute_value_id)
    if not attribute_value:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Значение атрибута не найдено',
        )
    return attribute_value

@service_attribute_router.delete(
    "attribute_values/{attribute_value_id}",
    status_code = status.HTTP_204_NO_CONTENT,
    summary="Удаление значения атрибута",
    description="Удаляет значение атрибута.",
)
async def delete_service_attribute_value(
        attribute_value_id: int,
        current_user: dict = Depends(get_current_user),
):
    if current_user["role"] not in ["admin", "master", "salon"]:
        raise HTTPException(status_code=403, detail="Недостаточно прав для выполнения операции.")

    await ServiceAttributeValueService.delete_attribute_value(attribute_value_id)

    return None

@service_attribute_router.put(
    "/attribute_values/{attribute_value_id}",
    response_model=ServiceAttributeValueCreateSchema,
    status_code=status.HTTP_200_OK,
    summary="Обновление значения атрибута",
    description="Обновление значения атрибута.",
)
async def update_service_attribute_value(
    attribute_value_id: int,
    data: ServiceAttributeValueCreateSchema,
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] not in ["admin", "master", "salon"]:
        raise HTTPException(status_code=403, detail="Недостаточно прав для выполнения операции.")

    # Получение текущего значения атрибута по его ID
    attribute_value = await ServiceAttributeValueService.get_or_none_attribute_value_id(attribute_value_id)
    if not attribute_value:
        raise HTTPException(status_code=404, detail="Значение атрибута не найден.")

    # Обновление значения атрибута через сервис
    updated_attribute_value = await ServiceAttributeValueService.update_attribute_value(
        attribute_value=attribute_value,
        name=data.name,
        slug=data.slug,
    )

    if not updated_attribute_value:
        raise HTTPException(status_code=500, detail="Не удалось обновить значение атрибута.")

    return updated_attribute_value

# Эндпоинт для привязки атрибута
@service_attribute_router.post(
    "/template_attributes",
    status_code=status.HTTP_201_CREATED,
    summary="Привязка атрибута к шаблону услуги",
    description="Позволяет создать связь между шаблоном услуги и атрибутом.",
)
async def attach_template_attribute(
    data: TemplateAttributeCreateSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Привязывает атрибут (тип+значение) к шаблону услуги.
    """
    # Проверка прав доступа
    if current_user["role"] not in ["admin", "master", "salon"]:
        raise HTTPException(status_code=403, detail="Недостаточно прав для выполнения операции.")

    # Вызываем сервисный метод
    template_attribute = await TemplateAttributeService.attach_attribute(data)
    return template_attribute

@service_attribute_router.get(
    "/template_attributes/{service_template_id}",
    status_code=status.HTTP_200_OK,
    summary="Получение всех атрибутов для шаблона услуги",
    description="Получение всех атрибутов для указанного шаблона услуги.",
)
async def list_template_attributes(
        service_template_id: int,
        current_user: dict = Depends(get_current_user),
):
    """
    Возвращает список атрибутов для указанного шаблона услуги.
    """
    if current_user["role"] not in ["admin", "master", "salon"]:
        raise HTTPException(status_code=403, detail="Недостаточно прав для выполнения операции.")

    # Получаем атрибуты для указанного шаблона услуги
    attributes =await TemplateAttributeService.get_list_by_service_template(service_template_id)
    return attributes