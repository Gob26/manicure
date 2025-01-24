from fastapi import APIRouter, Depends, File, HTTPException, status, Form, UploadFile

from db.models.photo_models.photo_standart_service_model import StandardServicePhoto
from use_case.photo_service.photo_base_servise import PhotoHandler
from db.schemas.service_schemas.service_standart_schemas import StandardServiceOut, StandardServiceCreate
from use_case.service_service.standart_service import StandardServiceService
from use_case.utils.permissions import check_user_permission
from use_case.utils.jwt_handler import get_current_user
from config.components.logging_config import logger


service_standart_router = APIRouter()

# Константы для организации структуры хранения
CITY_FOLDER = "default_city"  # Название папки для города
ROLE_FOLDER = "service"       # Название папки для роли
IMAGE_TYPE = "service_image"  # Тип изображения

@service_standart_router.post(
    "/services/standart",
    response_model=StandardServiceOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создание стандартной услуги",
    description="Создает новую стандартную услугу.",
)
async def create_service_standart_route(
    name: str = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    slug: str = Form(None),
    category_id: int = Form(...),
    image: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    # Проверка прав пользователя
    check_user_permission(current_user, ["admin", "master"])

    # Проверяем наличие изображения
    if not image:
        raise HTTPException(status_code=400, detail="Image file is required")

    try:
        # Загрузка фото
        photo_id = await PhotoHandler.add_photos_to_service(
            images=image,  # Поддержка одного изображения
            model=StandardServicePhoto,
            slug=slug,
            city=CITY_FOLDER,
            role=ROLE_FOLDER,
            image_type=IMAGE_TYPE
        )

        # Создаем услугу с photo_id
        service = await StandardServiceService.create_standart_service(
            name=name,
            title=title,
            content=content,
            slug=slug,
            category_id=category_id,
            default_photo_id=photo_id  # Добавляем photo_id при создании
        )

        return service

    except HTTPException as e:
        # Перехватываем ошибки обработки изображения или создания записи
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        # Логирование и обработка непредвиденных ошибок
        logger.error(f"Unexpected error in service creation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
