from fastapi import APIRouter, Depends, HTTPException, status
from use_case.utils.jwt_handler import get_current_user
from use_case.master_service.master_service import MasterService
from db.schemas.master_schemas.master_schemas import MasterCreateInputSchema, MasterCreateSchema
from config.components.logging_config import logger

master_router = APIRouter()

@master_router.post(
    "/master",
    response_model=MasterCreateSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создание профиля мастера",
    description="Создает новый профиль мастера.",
)
async def create_master_route(
    master_data: MasterCreateInputSchema,  # Данные для создания мастера (без user_id и city_id)
    current_user: dict = Depends(get_current_user)  # Получаем текущего пользователя
):
    logger.info(f"Текущий пользователь: {current_user}")

    # Проверка прав доступа
    if current_user["role"] not in ["master", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав для создания мастера"
        )

    # Создание мастера через сервис
    try:
        master = await MasterService.create_master(
            current_user=current_user,  # Передаем текущего пользователя
            **master_data.dict()  # Передаем данные мастера
        )
        return master  # Возвращаем данные созданного мастера
    except ValueError as ve:
        logger.warning(f"Ошибка бизнес-логики: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Системная ошибка при создании мастера: {e}")
        raise HTTPException(status_code=500, detail="Системная ошибка при создании мастера")
