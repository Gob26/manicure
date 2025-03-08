from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from typing import Optional, List
from pydantic.networks import HttpUrl

from db.models.photo_models.photo_avatar_model import AvatarPhotoMaster
from db.models.master_models.master_model import Master
from db.repositories.photo_repositories.photo_repository import PhotoRepository
from use_case.utils.jwt_handler import get_current_user
from use_case.master_service.master_service import MasterService
from db.schemas.master_schemas.master_schemas import MasterCreateInputSchema, MasterCreateSchema, MasterUpdateSchema
from use_case.photo_service.photo_base_servise import PhotoHandler
from config.components.logging_config import logger
from use_case.utils.permissions import check_user_permission

master_router = APIRouter()

@master_router.post("/",
    status_code=status.HTTP_201_CREATED,
    summary="Создание мастера",
    description="Создает новового мастера, используем Form."
)
async def create_master_route(
    title: str = Form(..., max_length=255),
    specialty: str = Form(..., max_length=255),
    experience_years: int = Form(0, ge=0),
    name: str = Form(..., max_length=255),
    slug: Optional[str] = Form(None, max_length=255),
    description: Optional[str] = Form(None),
    text: Optional[str] = Form(None),
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
    check_user_permission(current_user, ["admin", "master"])
    user_id = current_user.get("user_id")
    city_id = current_user.get("city_id")

    if not user_id or not city_id:
        raise HTTPException(status_code=400, detail="Ошибка аутентификации: данные пользователя отсутствуют.")

    try:
        master_data = MasterCreateInputSchema(
            title=title,
            specialty=specialty,
            description=description,
            text=text,
            experience_years=experience_years,
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

        master = await MasterService.create_master(
            user_id=user_id,
            city_id=city_id,
            **master_data.model_dump()
        )
        master_id = master.id

        photo_id = await PhotoHandler.add_photos_to_master(
            images=[image],
            master_id=master_id,
            model=AvatarPhotoMaster,
            city=str(city_id)
        )

        # Обновляем мастера, устанавливая avatar_id на ID первого загруженного фото
        if photo_id:
            master = await MasterService.update_master(current_user=current_user, master_id=master_id, avatar_id=[0])
        else:
            logger.warning(f"Фото не загружено для мастера с ID {master_id}.")

        return master

    except ValueError as ve:
        logger.warning(f"Ошибка валидации: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        logger.error(f"Системная ошибка при создании мастера: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


# Обновление профиля мастера
#Обновление профиля мастера
@master_router.put(
    "/{master_id}",
    status_code=status.HTTP_200_OK,
    summary="Обновление профиля мастера",
    description="Обновляет существующий профиль мастера с новыми данными.",
)
async def update_master_route(
    master_id: int,
    title: Optional[str] = Form(None, max_length=255),
    specialty: Optional[str] = Form(None, max_length=255),
    experience_years: Optional[int] = Form(None, ge=0),
    name: Optional[str] = Form(None, max_length=255),
    slug: Optional[str] = Form(None, max_length=255),
    description: Optional[str] = Form(None),
    text: Optional[str] = Form(None),
    address: Optional[str] = Form(None, max_length=256),
    phone: Optional[str] = Form(None, max_length=20),
    telegram: Optional[str] = Form(None),
    whatsapp: Optional[str] = Form(None),
    website: Optional[str] = Form(None),
    vk: Optional[str] = Form(None),
    instagram: Optional[str] = Form(None),
    accepts_at_home: Optional[bool] = Form(None),
    accepts_in_salon: Optional[bool] = Form(None),
    accepts_offsite: Optional[bool] = Form(None),
    image: Optional[UploadFile] = File(None),
    current_user: dict = Depends(get_current_user),
):
    """Обновление данных мастера (включая фото)."""

    logger.critical("ВХОД В ФУНКЦИЮ UPDATE_MASTER_ROUTE - ПРОВЕРКА ЗАПУСКА КОДА?") # <----  ТЕСТ "HELLO WORLD" - Оставьте пока для уверенности
    logger.debug(f"master_id parameter: {master_id}")
    check_user_permission(current_user, ["admin", "master"])
    user_id = current_user.get("user_id")
    city_id = current_user.get("city_id")

    if not user_id or not city_id:
        raise HTTPException(status_code=400, detail="Ошибка аутентификации: данные пользователя отсутствуют.")

    try:
        # Проверяем, есть ли мастер
        master = await MasterService.get_master_by_id(master_id)
        if not master:
            raise HTTPException(status_code=404, detail="Мастер не найден")
        if str(master.user_id) != str(user_id):
            raise HTTPException(status_code=403, detail="Нет прав на обновление")

        # Формируем объект обновления
        master_data = MasterUpdateSchema(
            title=title,
            specialty=specialty,
            description=description,
            text=text,
            experience_years=experience_years,
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

        # Обновляем мастера
        updated_master = await MasterService.update_master(
            current_user=current_user,
            master_id=master_id,
            **master_data.model_dump()
        )

        logger.debug(f"Значение image перед if image: {image}") # <----  НОВОЕ ОТЛАДОЧНОЕ СООБЩЕНИЕ (ПЕРЕД if image:)


        # Если есть новое изображение
        if image:
            logger.info(f"Обновляем фото мастера {master_id}")
            logger.debug(f"Тип параметра image: {type(image)}") # <----  ОТЛАДОЧНЫЕ СООБЩЕНИЯ ДЛЯ IMAGE (ВНУТРИ if image:)
            logger.debug(f"Значение параметра image: {image}") # <----  ОТЛАДОЧНЫЕ СООБЩЕНИЯ ДЛЯ IMAGE (ВНУТРИ if image:)


            # Находим старое фото
            old_photo = await PhotoRepository.get_photo(AvatarPhotoMaster, master_id=master_id)

            # Удаляем фото из базы и физически
            if old_photo:
                await PhotoHandler.delete_photo(model=AvatarPhotoMaster,photo_id=old_photo.id)

            # Загружаем новое фото
            photo_id = await PhotoHandler.add_photos_to_master(
                images=[image],
                master_id=master_id,
                model=AvatarPhotoMaster,
                city=str(city_id)
            )

            #Устанавливаем новую фотографию как аватарку
            if photo_id:
                updated_master = await MasterService.update_master(current_user=current_user, master_id=master_id, avatar_id=[0])
            else:
                logger.warning(f"Фото не загружено для мастера с ID {master_id}.")

        return updated_master

    except ValueError as ve:
        logger.warning(f"Ошибка валидации: {ve}")
        raise HTTPException(status_code=400, detail="Ошибка валидации данных: " + str(ve))


    except Exception as e:
        logger.error(f"Системная ошибка при создании мастера: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


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