from typing import List, Optional
from fastapi import APIRouter, Depends, File, HTTPException, status, Form, UploadFile


from db.schemas.service_schemas.service_custom_schemas import CustomServiceOut, CustomServiceCreate, CustomServiceUpdate
from use_case.service_service.custom_service import CustomServiceService
from use_case.utils.permissions import check_user_permission
from use_case.utils.jwt_handler import get_current_user
from config.components.logging_config import logger


service_custom_router = APIRouter()

@service_custom_router.post(
    "/", 
    response_model=CustomServiceOut, 
    status_code=status.HTTP_201_CREATED,
    summary="Создание новой услуги",
    description="Создает новую услугу.",
    )

async def create_custom_service_route(
    standard_service_id: int = Form(..., description="ID стандартной услуги"),
    base_price: float = Form(..., description="Базовая стоимость услуги"),
    duration_minutes: int = Form(..., description="Длительность услуги в минутах"),
    description: Optional[str] = Form(None, description="Описание услуги"),
    photos: Optional[List[UploadFile]] = File(None, description="Фото для услуги"),
    current_user: dict = Depends(get_current_user),
):
    # Проверка прав пользователя
    check_user_permission(current_user, ["admin", "master", "salon"])

    try:
        service = await CustomServiceService.create_custom_service(
            current_user=current_user,
            standard_service_id=standard_service_id,
            base_price=base_price,
            duration_minutes=duration_minutes,
            description=description,
            images=photos,
            master_id=None,
            salon_id = None,
        )
        return service
    except ValueError as e:
        logger.warning(f"Ошибка бизнес-логики: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Системная ошибка при создании услуги: {e}")
        raise HTTPException(status_code=500, detail="Системная ошибка при создании услуги")


@service_custom_router.put(
    "/{custom_service_id}",
    response_model=CustomServiceOut,
    status_code=status.HTTP_200_OK,
    summary="Обновление услуги",
    description="Обновляет существующую услугу.",
)

async def update_custom_service_route(
    custom_service_id: int,
    updated_service_data: CustomServiceUpdate = Depends(),
    photos: Optional[List[UploadFile]] = File(None, description="Новые фото для услуги"),
    current_user: dict = Depends(get_current_user),
):
    logger.info(f"Текущий пользователь: {current_user}")

    # Проверка прав доступа
    check_user_permission(current_user, ["admin", "master", "salon"])

    try:
        updated_service = await CustomServiceService.update_custom_service(
            custom_service_id=custom_service_id,
            updated_service_data=updated_service_data.dict(exclude_unset=True), # exclude_unset, чтобы не затереть существующие значения в базе данных
            images=photos,
            current_user=current_user
        )
        return updated_service
    except ValueError as e:
        logger.warning(f"Ошибка бизнес-логики: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Системная ошибка при обновлении услуги: {e}")
        raise HTTPException(status_code=500, detail="Системная ошибка при обновлении услуги")

    

    