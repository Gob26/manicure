from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from typing import Optional, List
from pydantic.networks import HttpUrl

from db.models.photo_models.photo_avatar_model import AvatarPhotoMaster
from db.models.master_models.master_model import Master
from use_case.utils.jwt_handler import get_current_user
from use_case.master_service.master_service import MasterService
from db.schemas.master_schemas.master_schemas import MasterCreateInputSchema, MasterCreateSchema
from use_case.photo_service.photo_base_servise import PhotoHandler
from config.components.logging_config import logger
from use_case.utils.permissions import check_user_permission

# Константы для организации структуры хранения
CITY_FOLDER = "default_city"  # Название папки для города
ROLE_FOLDER = "master"  # Название папки для роли
IMAGE_TYPE = "avatar"

master_router = APIRouter()


@master_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создание профиля мастера",
    description="Создает новый профиль мастера с контактной информацией, соцсетями и вариантами приема."
                "Данные передаются в формате multipart/form-data",
)
async def create_master_route(
    title: Optional[str] = Form(..., max_length=255),
    description: Optional[str] = Form(None),
    text: Optional[str] = Form(None),
    experience_years: int = Form(..., ge=0),
    specialty: str = Form(..., max_length=255),
    slug: str = Form(..., max_length=255),
    name: str = Form(..., max_length=255),
    address: Optional[str] = Form(None, max_length=256),
    phone: Optional[str] = Form(None, max_length=20),
    telegram: Optional[HttpUrl] = Form(None),
    whatsapp: Optional[HttpUrl] = Form(None),
    website: Optional[HttpUrl] = Form(None),
    vk: Optional[HttpUrl] = Form(None),
    instagram: Optional[HttpUrl] = Form(None),
    accepts_at_home: bool = Form(False),
    accepts_in_salon: bool = Form(False),
    accepts_offsite: bool = Form(False),
    image: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    # Создаем объект Pydantic модели для валидации данных
    master_data = MasterCreateInputSchema(
        title=title,
        description=description,
        text=text,
        experience_years=experience_years,
        specialty=specialty,
        slug=slug,
        name=name,
        address=address,
        phone=phone,
        telegram=telegram,
        whatsapp=whatsapp,
        website=website,
        vk=vk,
        instagram=instagram,
        accepts_at_home=accepts_at_home,
        accepts_in_salon=accepts_in_salon,
        accepts_offsite=accepts_offsite,
    )

    user_id = current_user.get("user_id")
    city_id = current_user.get("city_id")

    if not user_id or not city_id:
        raise HTTPException(status_code=400, detail="Не удалось извлечь данные пользователя.")

    try:
        avatar_id = await PhotoHandler.add_photos_to_service(
            images=image,
            model=AvatarPhotoMaster,
            slug=master_data.slug,
            city=CITY_FOLDER,
            role=ROLE_FOLDER,
            image_type=IMAGE_TYPE,
        )

        master = await MasterService.create_master(
            user_id=user_id,
            city_id=city_id,
            avatar_id=avatar_id,
            **master_data.dict()
        )

        return master

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Системная ошибка при создании мастера: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Системная ошибка при создании мастера")


#Обновление профиля мастера
@master_router.put(
    "/{master_id}",
    response_model=MasterCreateSchema,
    summary="Обновление профиля мастера",
    description="Обновляет существующий профиль мастера с новыми данными.",
)
async def update_master_route(
    master_id: int,
    master_data: MasterCreateInputSchema,
    current_user: dict = Depends(get_current_user),
):
    logger.info(f"Текущий пользователь: {current_user}")

    # Проверка прав доступа
    check_user_permission(current_user, ["master", "admin"])

    # Обновление мастера через сервис
    try:
        master = await MasterService.update_master(
            master_id=master_id,
            current_user=current_user,
            **master_data.dict()
        )
        return master
    except ValueError as ve:
        logger.warning(f"Ошибка бизнес-логики: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Системная ошибка при обновлении мастера: {e}")
        raise HTTPException(status_code=500, detail="Системная ошибка при обновлении мастера")
    
# Удаление профиля мастера
@master_router.delete(
    "/{master_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление профиля мастера",
    description="Удаляет профиль мастера по его ID.",
)
async def delete_master_route(
    master_id: int,
    current_user: dict = Depends(get_current_user),
):
    logger.info(f"Текущий пользователь: {current_user}")

    # Проверка прав доступа
    check_user_permission(current_user, ["master", "admin"])

    # Удаление мастера через сервис
    try:
        await MasterService.delete_master(master_id=master_id, current_user=current_user)
    except ValueError as ve:
        logger.warning(f"Ошибка бизнес-логики: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Системная ошибка при удалении мастера: {e}")
        raise HTTPException(status_code=500, detail="Системная ошибка при удалении мастера")