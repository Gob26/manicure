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
        logger.error(f"Ошибка при создании салона: {e}")

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