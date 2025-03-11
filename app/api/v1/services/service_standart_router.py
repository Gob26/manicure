from fastapi import APIRouter, Depends, File, HTTPException, status, Form, UploadFile

from db.models.photo_models.photo_standart_service_model import StandardServicePhoto
from use_case.photo_service.photo_base_servise import PhotoHandler
from db.schemas.service_schemas.service_standart_schemas import StandardServiceOut, StandardServiceCreate, \
    StandardServiceUpdate
from use_case.service_service.standart_service import StandardServiceService
from use_case.utils.permissions import check_user_permission
from use_case.utils.jwt_handler import get_current_user
from config.components.logging_config import logger


service_standart_router = APIRouter()

# Константы для организации структуры хранения фотографий стандартных услуг
CITY_FOLDER = " all_city"  # Название папки для города


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
    description: str = Form(...),
    content: str = Form(...),
    slug: str = Form(None),
    category_id: int = Form(...),
    image: UploadFile | None = File(None),
    current_user: dict = Depends(get_current_user),
):
    # Проверка прав пользователя
    check_user_permission(current_user, ["admin", "master"])

    try:
        service_data = StandardServiceCreate(
            name=name,
            title=title,
            description=description,
            content=content,
            slug=slug,
            category_id=category_id,
        )
        logger.debug(f"create_service_standart_route: service_data создан: {service_data}")

        # Создаем услугу без фотографий
        logger.debug(f"create_service_standart_route: Вызов StandardServiceService.create_standart_service с данными: {service_data.model_dump()}")
        service = await StandardServiceService.create_standart_service(
            **service_data.model_dump()
        )
        logger.debug(f"create_service_standart_route: StandardServiceService.create_standart_service вернул услугу: {service}")


        service_id = service.id
        logger.debug(f"create_service_standart_route: Услуга создана с ID: {service_id}")

        photo_ids = await PhotoHandler.add_photos_to_service(
            images=[image],
            service_id=service_id,
            model=StandardServicePhoto,
            city=CITY_FOLDER,
        )
        logger.debug(f"create_service_standart_route: PhotoHandler.add_photos_to_service вернул photo_ids: [photo_ids]")


        if photo_ids:
            update_data = StandardServiceUpdate(
                name=name,
                title=title,
                description=description,
                content=content,
                slug=slug,
                category_id=category_id,
                standard_services_id=photo_ids[0]
            )
            logger.debug(f"create_service_standart_route: update_data для обновления фото создан: {update_data}")

            logger.debug(f"create_service_standart_route: Calling StandardServiceService.update_standart_service "
                         f"with service_id={service_id}, update_data={update_data}")
            update_service = await StandardServiceService.update_standart_service(  # <---- Исправленный вызов!
                service_id=service_id,
                schema=update_data, # <----  Передаем update_data как schema!
            )
            logger.debug(f"create_service_standart_route: StandardServiceService.update_standart_service вернул обновленную услугу: {service}")

        else:
            logger.warning(f"Фото для сервиса salon_id={service_id} не было загружено.")
            update_service = service
        logger.info(f"create_service_standart_route: Процесс создания стандартной услуги успешно завершен.")
        return update_service

    except ValueError as ve:
        logger.warning(f"create_service_standart_route: ValueError: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"create_service_standart_route: Системная ошибка при создании сервиса: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Системная ошибка при создании сервиса")


@service_standart_router.post(
    "/services/{service_id}"
    status_code=status.HTTP_200_OK,
    summary="Обновление информации о стандартной услуге",
    description="Обновляет информацию и фотографии стандартной услуги.",
)
async def update_service_standart_route(
    service_id: int,
    name: Optional[str] = Form(None),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    content: Optional[str] = Form(None),
    slug: Optional[str] = Form(None),
    category_id: Optional[int] = Form(None),
    image: Optional[UploadFile] = File(None),
    current_user: dict = Depends(get_current_user),
):
    check_user_permission(current_user, ["admin", "master"])

    service = StandardServiceService.get