from fastapi import APIRouter, Depends, HTTPException, status
from use_case.utils.jwt_handler import get_current_user
from use_case.master_service.master_service import MasterService
from db.schemas.master_schemas.master_schemas import MasterCreateInputSchema, MasterCreateSchema
from config.components.logging_config import logger
from use_case.utils.permissions import check_user_permission

master_router = APIRouter()

@master_router.post(
    "/",
    response_model=MasterCreateSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создание профиля мастера",
    description="Создает новый профиль мастера с контактной информацией, соцсетями и вариантами приема.",
)
async def create_master_route(
    master_data: MasterCreateInputSchema,  # Данные для создания мастера
    current_user: dict = Depends(get_current_user),  # Получаем текущего пользователя
):
    logger.info(f"Текущий пользователь: {current_user}")

    # Проверка прав доступа
    check_user_permission(current_user, ["master", "admin"])

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

#Обновление профиля мастера
@master_router.put(
    "/{master_id}",
    response_model=MasterCreateSchema,
    summary="Обновление профиля мастера",
    description="Обновляет существующий профиль мастера с новыми данными.",
)
async def update_master_route(
    master_id: int,
    master_data: MasterCreateInputSchema,
    current_user: dict = Depends(get_current_user),
):
    logger.info(f"Текущий пользователь: {current_user}")

    # Проверка прав доступа
    check_user_permission(current_user, ["master", "admin"])

    # Обновление мастера через сервис
    try:
        master = await MasterService.update_master(
            master_id=master_id,
            current_user=current_user,
            **master_data.dict()
        )
        return master
    except ValueError as ve:
        logger.warning(f"Ошибка бизнес-логики: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Системная ошибка при обновлении мастера: {e}")
        raise HTTPException(status_code=500, detail="Системная ошибка при обновлении мастера")
    
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