from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from typing import Optional
from pydantic.networks import HttpUrl

from db.models import AvatarPhotoSalon
from use_case.photo_service.photo_base_servise import PhotoHandler
from use_case.utils.jwt_handler import get_current_user
from use_case.salon_service.salon_service import SalonService
from db.schemas.salon_schemas.salon_schemas import SalonCreateSchema, SalonCreateInputSchema, SalonUpdateSchema
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
    check_user_permission(current_user, ["admin", "salon"])

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

        # Создаем салон без аватарки сначала
        salon = await SalonService.create_salon(
            user_id=user_id,
            city_id=city_id,
            **salon_data.dict()
        )
        salon_id = salon.id

        # Загружаем фото и получаем список photo_ids
        photo_ids = await PhotoHandler.add_photos_to_salon(
            images=[image],
            salon_id=salon_id,
            model=AvatarPhotoSalon,
            city=str(city_id),
        )

        # Обновляем салон, устанавливая avatar_id на ID первого загруженного фото
        if photo_ids:
            salon = await SalonService.update_salon(current_user=current_user,salon_id=salon_id, avatar_id=photo_ids[0])
        else:
            logger.warning(f"Фото для салона salon_id={salon_id} не было загружено.")

        return salon

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Системная ошибка при создании салона: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Системная ошибка при создании салона")

@salon_router.put(
        "/{salon_id}",
    status_code=status.HTTP_200_OK,
    summary="Обновление салона",
    description="Обновляет существующий салон.",
)
async def update_salon_route(
    salon_id: int,
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
    logger.info(f"Текущий пользователь: {current_user}")

    # Проверка прав доступа
    check_user_permission(current_user, ["salon", "admin"])
    user_id = current_user.get("user_id")
    city_id = current_user.get("city_id")

    if not user_id or not city_id:
        raise HTTPException(status_code=400, detail="Не удалось извлечь данные пользователя.")

    try:
        salon = await SalonService.get_salon_by_id(salon_id)
        if not salon:
            raise HTTPException(status_code=404, detail="Салон не найден")
        if salon.user_id != user_id:
            raise HTTPException(status_code=403, detail="Недостаточно прав для обновления салона")
        
        salon_data = SalonUpdateSchema(
            name=name,
            title=title,
            slug=slug,
            description=description,
            text=text,
            address=address,
            phone=phone,
            telegram=telegram,
            whatsapp=whatsapp,
            website=website,
            vk=vk,
            instagram=instagram,
            
        )
    
        updated_salon = await SalonService.update_salon(
            current_user=current_user,
            salon_id=salon_id,
            **salon_data.dict()
        )

        logger.debug(f"Значение image перед if image: {image}") 

            # Если есть новое изображение
        if image:
            logger.info(f"Обновляем фото мастера {master_id}")
            logger.debug(f"Тип параметра image: {type(image)}")
            logger.debug(f"Значение параметра image: {image}")

            old_photo = await PhotoHandler.get_photo_by_id(model=AvatarPhotoSalon, salon_id=salon_id)

            if old_photo:
                await PhotoHandler.delete_photo_by_id(model=AvatarPhotoSalon, photo_id=old_photo.id)

            photo_id = await PhotoHandler.add_photos_to_salon(
                images=[image],
                salon_id=salon_id,
                model=AvatarPhotoSalon,
                city=str(city_id),
            )

            #Устанавливаем новую фотографию как аватарку
            if photo_id:
                updated_salon = await SalonService.update_salon(
                    current_user=current_user,
                    salon_id=salon_id,
                    avatar_id=[0]
                )
            else:
                logger.warning(f"Фото для салона salon_id={salon_id} не было загружено.")

        return updated_salon
        
    except ValueError as ve:
        logger.warning(f"Ошибка валидации: {ve}")
        raise HTTPException(status_code=400, detail="Ошибка валидации данных: " + str(ve))

    except Exception as e:
        logger.error(f"Системная ошибка при создании мастера: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


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