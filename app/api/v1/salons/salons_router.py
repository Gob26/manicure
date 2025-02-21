from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from typing import Optional, List
from pydantic.networks import HttpUrl

from db.models import AvatarPhotoSalon
from use_case.photo_service.photo_base_servise import PhotoHandler
from use_case.utils.jwt_handler import get_current_user
from use_case.salon_service.salon_service import SalonService
from db.schemas.salon_schemas.salon_schemas import SalonCreateSchema, SalonCreateInputSchema
from config.components.logging_config import logger
from use_case.utils.permissions import check_user_permission

# Константы для организации структуры хранения
CITY_FOLDER = "default_city"  # Название папки для города
ROLE_FOLDER = "master"  # Название папки для роли
IMAGE_TYPE = "avatar"
salon_router = APIRouter()

@salon_router.post("/",
    response_model=SalonCreateSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создание салона",
    description="Создает новый салон, используем Form.",
)
async def create_salon_route(
    name: str = Form(..., max_length=255, description="Имя салона"),
    title: str = Form(..., max_length=255, description="Тайтл салона"),
    slug: Optional[str] = Form(None, max_length=255, description="Уникальный идентификатор"),
    description: Optional[str] = Form(None, description="Описание салона"),
    text: Optional[str] = Form(None, description="Дополнительный текст"),
    address: str = Form(..., max_length=256, description="Адрес салона"),
    phone: str = Form(..., max_length=20, description="Телефон салона"),
    telegram: Optional[HttpUrl] = Form(None, description="Telegram салона"),
    whatsapp: Optional[HttpUrl] = Form(None, description="WhatsApp салона"),
    website: Optional[HttpUrl] = Form(None, description="Веб-сайт салона"),
    vk: Optional[HttpUrl] = Form(None, description="ВКонтакте салона"),
    instagram: Optional[HttpUrl] = Form(None, description="Instagram салона"),
    image: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """Создание профиля салона с валидацией данных."""
    user_id = current_user.get("user_id")
    city_id = current_user.get("city_id")

    if not user_id or not city_id:
        raise HTTPException(status_code=400, detail="Не удалось извлечь данные пользователя.")
    try:
        # Создаем объект Pydantic модели для валидации данных
        salon_data = SalonCreateInputSchema(
            title=title,
            description=description,
            text=text,
            slug=slug,
            name=name,
            address=address,
            phone=phone,
            telegram=telegram,
            whatsapp=whatsapp,
            website=website,
            vk=vk,
            instagram=instagram,
        )

        avatar_id = await PhotoHandler.add_photos_to_service(
            images=[image],
            model=AvatarPhotoSalon,
            slug=salon_data.slug,
            city=CITY_FOLDER,
            role=ROLE_FOLDER,
            image_type=IMAGE_TYPE,
        )

        salon = await SalonService.create_salon(
            user_id=user_id,
            city_id=city_id,
            avatar_id=avatar_id,
            **salon_data.dict()
        )

        return salon

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Системная ошибка при создании мастера: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Системная ошибка при создании мастера")

@salon_router.put("/{salon_id}",
    response_model=SalonCreateSchema,
    status_code=status.HTTP_200_OK,
    summary="Обновление салона",
    description="Обновляет существующий салон.",
)
async def update_salon_route(
    salon_id: int,
    salon_data: SalonCreateInputSchema,
    current_user: dict = Depends(get_current_user)
):
    logger.info(f"Текущий пользователь: {current_user}")

    # Проверка прав доступа
    check_user_permission(current_user, ["salon", "admin"])

    try:
        salon = await SalonService.update_salon(
            current_user=current_user,
            salon_id=salon_id,
            **salon_data.dict()
        )
        return salon
    except ValueError as e:
        logger.warning(f"Ошибка бизнес-логики: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Системная ошибка при обновлении салона: {e}")
        raise HTTPException(status_code=500, detail="Системная ошибка при обновлении салона")    
    
@salon_router.delete("/{salon_id}",
    status_code=status.HTTP_200_OK,
    summary="Удаление салона",
    description="Удаляет салон по его ID.",
)
async def delete_salon_route(
    salon_id: int,
    current_user: dict = Depends(get_current_user)
):
    logger.info(f"Текущий пользователь: {current_user}")

    # Проверка прав доступа
    check_user_permission(current_user, ["salon", "admin"])

    try:
        salon = await SalonService.delete_salon(
            current_user=current_user,
            salon_id=salon_id
        )
        return salon
    except ValueError as e:
        logger.warning(f"Ошибка бизнес-логики: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Системная ошибка при удалении салона: {e}")
        raise HTTPException(status_code=500, detail="Системная ошибка при удалении салона")