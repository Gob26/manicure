from fastapi import APIRouter, Depends, HTTPException, status
from use_case.utils.jwt_handler import get_current_user
from use_case.salon_service.salon_service import SalonService
from db.schemas.salon_schemas.salon_schemas import SalonCreateSchema, SalonCreateInputSchema
from config.components.logging_config import logger
from use_case.utils.permissions import check_user_permission

salon_router = APIRouter()

@salon_router.post("/",
    response_model=SalonCreateSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создание салона",
    description="Создает новый салон.", 
)
async def create_salon_route(
    salon_data: SalonCreateInputSchema, # Данные для создания салона (без user_id и city_id)
    current_user: dict = Depends(get_current_user) # Получаем текущего пользователя
):
    logger.info(f"Текущий пользователь: {current_user}")

    # Проверка прав доступа
    check_user_permission(current_user,["salon", "admin"])

    # Создание салона через сервис
    try:
        salon = await SalonService.create_salon(
            current_user=current_user,  # Передаем текущего пользователя
            **salon_data.dict()  # Передаем данные салона   
        )
        return salon  # Возвращаем данные созданного салона
    except ValueError as e:
        logger.warning(f"Ошибка бизнес-логики: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Системная ошибка при создании салона: {e}")
        raise HTTPException(status_code=500, detail="Системная ошибка при создании салона")