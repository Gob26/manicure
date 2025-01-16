from fastapi import APIRouter, Depends, File, HTTPException, status, Form, UploadFile

from db.models import StandardServicePhoto
from use_case.photo_service.photo_base_servise import PhotoHandler
from db.schemas.service_schemas.service_standart_schemas import StandardServiceOut, StandardServiceCreate
from use_case.service_service.standart_service import StandardServiceService
from use_case.utils.permissions import check_user_permission
from use_case.utils.jwt_handler import get_current_user

service_standart_router = APIRouter()

@service_standart_router.post(
    "/services/standart",
    response_model=StandardServiceOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_service_standart_route(
    name: str = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    slug: str = Form(...),
    category_id: int = Form(...),
    image: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    check_user_permission(current_user, ["admin", "master"])

    if image is None:
        raise HTTPException(status_code=400, detail="Image file is required")

    # Сначала загружаем фото
    photo_id = await PhotoHandler.add_photo_to_service(
    image=image,
    model=StandardServicePhoto,  # Передаём модель
    slug=slug,
    city="Moscow",
    role="service",
    image_type="service_image"
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

